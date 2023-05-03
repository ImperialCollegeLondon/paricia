# -*- coding: utf-8 -*-

################################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos (iMHEA)
# basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#         Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS), Ecuador.
#         Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones creadoras,
#              ya sea en uso total o parcial del código.

import datetime

import utm
from django.apps import apps
from django.db import connection

from calidad.functions import construir_intervalos_freq
from calidad.models import *
from estacion.models import Estacion
from frecuencia.models import Frecuencia
from home.functions import *
from medicion.models import PolarWind
from telemetria.models import (
    AlarmaEstado,
    ConfigCalidad,
    ConfigVisualizar,
    PrecipitacionAcumulada,
    PrecipitacionEventos,
    PrecipitacionMultianual,
    TeleVariables,
)
from variable.models import Variable


def consulta(estacion_id, inicio):
    config = ConfigVisualizar.objects.filter(estacion_id=estacion_id)
    variables = Variable.objects.filter(pk__in=config.values("variable_id").distinct())
    estacion = Estacion.objects.get(pk=estacion_id).est_codigo

    fechahora_actual = datetime.datetime.now()
    if inicio is None:
        inicio = fechahora_actual.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        inicio = datetime.datetime.strptime(inicio, "%Y-%m-%d")

    lista = {}
    viento = False
    for v in variables:
        ### Dirección viento o velocidad
        if v.var_id in (4, 5):
            viento = True
            continue

        Crudo = apps.get_model(
            app_label="medicion", model_name="Var" + str(v.var_id) + "Medicion"
        )
        tabla = "medicion_var" + str(v.var_id) + "medicion"
        sql = (
            "SELECT * FROM "
            + tabla
            + " WHERE estacion_id = %s AND fecha>= %s AND fecha<= %s AND valor IS NOT NULL "
            "order by fecha ASC;"
        )
        consulta = Crudo.objects.raw(sql, [estacion_id, inicio, fechahora_actual])

        valor = []
        fecha = []
        fecha_anterior = None
        for fila in consulta:
            if fecha_anterior is None:
                valor.append(fila.valor)
                fecha.append(fila.fecha)
                fecha_anterior = fila.fecha
                continue

            diff_dt = fila.fecha - fecha_anterior
            if diff_dt.seconds > 300 or diff_dt.days > 0:
                valor.append(None)
                fecha.append(fecha_anterior + datetime.timedelta(minutes=5))
            valor.append(fila.valor)
            fecha.append(fila.fecha)
            fecha_anterior = fila.fecha

        datos = {"valor": valor, "fecha": fecha}
        umbral_superior = config.get(variable_id=v.var_id).umbral_superior
        umbral_superior = float(umbral_superior) if umbral_superior else None
        umbral_inferior = config.get(variable_id=v.var_id).umbral_inferior
        umbral_inferior = float(umbral_inferior) if umbral_inferior else None

        lista[v.var_id] = {
            "estacion": estacion,
            "var_nombre": v.var_nombre,
            "var_unidad": v.uni_id.uni_sigla,
            "datos": datos,
            "umbral_superior": umbral_superior,
            "umbral_inferior": umbral_inferior,
        }
    if viento:
        sql = """
SELECT ROW_NUMBER() OVER (ORDER BY vvi.fecha) AS id, 
    vvi.fecha AS fecha, vvi.valor AS velocidad, dvi.valor AS direccion 
FROM medicion_var4medicion vvi, medicion_var5medicion dvi
WHERE vvi.estacion_id = %s AND vvi.fecha>= %s AND vvi.fecha<= %s 
AND dvi.fecha = vvi.fecha AND dvi.estacion_id = vvi.estacion_id 
AND vvi.valor IS NOT NULL AND dvi.valor IS NOT NULL 
ORDER BY fecha ASC
        """
        consulta = PolarWind.objects.raw(sql, [estacion_id, inicio, fechahora_actual])
        velocidad = []
        direccion = []
        for fila in consulta:
            velocidad.append(fila.velocidad)
            direccion.append(fila.direccion)

        datos = {"velocidad": velocidad, "direccion": direccion}
        lista[405] = {
            "estacion": estacion,
            "var_nombre": "Viento",
            "var_unidad": "m/s y grados",
            "datos": datos,
            "umbral_superior": config.get(variable_id=v.var_id).umbral_superior,
            "umbral_inferior": config.get(variable_id=v.var_id).umbral_inferior,
        }
    return lista


def consulta_calidad(estacion_id, inicio, usuario):
    config = ConfigCalidad.objects.filter(estacion_id=estacion_id)
    variables = Variable.objects.filter(pk__in=config.values("variable_id").distinct())
    if usuario.username != "admin":
        usrvar = UsuarioVariable.objects.get(usuario=usuario)
        variables = variables.filter(pk__in=usrvar.variable.values("var_id"))
    estacion = Estacion.objects.get(pk=estacion_id).est_codigo

    fechahora_actual = datetime.datetime.now()
    if inicio is None:
        inicio = fechahora_actual.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        inicio = datetime.datetime.strptime(inicio, "%Y-%m-%d")

    lista = {}
    frecuencias = Frecuencia.objects.filter(est_id=estacion_id)

    for v in variables:
        Crudo = apps.get_model(
            app_label="medicion", model_name="Var" + str(v.var_id) + "Medicion"
        )
        tabla = "medicion_var" + str(v.var_id) + "medicion"
        sql = (
            "SELECT * FROM "
            + tabla
            + " WHERE estacion_id = %s AND fecha>= %s AND fecha<= %s AND valor IS NOT NULL "
            "order by fecha ASC, profundidad ASC;"
        )
        consulta = Crudo.objects.raw(sql, [estacion_id, inicio, fechahora_actual])

        sql2 = (
            "SELECT DISTINCT(profundidad) FROM "
            + tabla
            + " WHERE estacion_id = %s order by profundidad ASC;"
        )
        with connection.cursor() as cursor:
            cursor.execute(sql2, [estacion_id])
            profundidades = cursor.fetchall()

        niveles = {}
        for p in profundidades:
            n = p[0]
            _niveles = {
                "valor": [],
                "fecha": [],
                "fecha_anterior": None,
                "umbral_superior": None,
                "umbral_inferior": None,
            }
            niveles[n] = objdict(_niveles)
            umbral_superior = config.get(
                variable_id=v.var_id, profundidad=n
            ).umbral_superior
            niveles[n].umbral_superior = (
                float(umbral_superior) if umbral_superior else None
            )
            umbral_inferior = config.get(
                variable_id=v.var_id, profundidad=n
            ).umbral_inferior
            niveles[n].umbral_inferior = (
                float(umbral_inferior) if umbral_inferior else None
            )
        frec_list = (
            frecuencias.filter(var_id=v)
            .order_by("fre_fecha_ini")
            .values_list("fre_fecha_ini", "fre_valor", named=True)
        )
        frec_list = construir_intervalos_freq(frec_list, inicio, fechahora_actual)
        try:
            intervalo_frecuencia = frec_list.pop()
        except:
            continue
        frec_segundos = intervalo_frecuencia["freq"] * 60

        for fila in consulta:
            if niveles[fila.profundidad].fecha_anterior is None:
                niveles[fila.profundidad].valor.append(fila.valor)
                niveles[fila.profundidad].fecha.append(fila.fecha)
                niveles[fila.profundidad].fecha_anterior = fila.fecha
                continue

            diff_dt = fila.fecha - niveles[fila.profundidad].fecha_anterior
            while not (
                intervalo_frecuencia["inicio"]
                <= fila.fecha
                < intervalo_frecuencia["fin"]
            ):
                intervalo_frecuencia = frecuencias.pop()
                frec_segundos = intervalo_frecuencia["freq"] * 60

            if diff_dt.seconds > (frec_segundos + 40) or diff_dt.days > 0:
                niveles[fila.profundidad].valor.append(None)
                niveles[fila.profundidad].fecha.append(
                    niveles[fila.profundidad].fecha_anterior
                    + datetime.timedelta(minutes=int(frec_segundos / 60))
                )
            niveles[fila.profundidad].valor.append(fila.valor)
            niveles[fila.profundidad].fecha.append(fila.fecha)
            niveles[fila.profundidad].fecha_anterior = fila.fecha

        lista[v.var_id] = {
            "estacion": estacion,
            "var_nombre": v.var_nombre,
            "var_unidad": v.uni_id.uni_sigla,
            "datos_niveles": niveles,
        }

    return lista


def consulta_alarma_transmision():
    resultado = {}
    try:
        lim_inf_horas = TeleVariables.objects.get(nombre="ALAR_TRAN_LIMI_INFE").valor
        lim_sup_horas = TeleVariables.objects.get(nombre="ALAR_TRAN_LIMI_SUPE").valor
    except:
        lim_inf_horas = ""
        lim_sup_horas = ""
    resultado["limites"] = {"lim1": lim_inf_horas, "lim2": lim_sup_horas}

    estaciones = (
        AlarmaEstado.objects.filter(
            estacion_id__in=ConfigVisualizar.objects.order_by()
            .values("estacion_id")
            .distinct()
        )
        .order_by("estacion_id", "-fecha")
        .distinct("estacion_id")
    )
    resultado["estaciones"] = {}

    for e in estaciones:
        easting = float(e.estacion.est_longitud)
        northing = float(e.estacion.est_latitud)
        coordenadas = utm.to_latlon(easting, northing, 17.41666, "M")
        estacion = {
            "codigo": e.estacion.est_codigo,
            "latitud": coordenadas[0],
            "longitud": coordenadas[1],
            "estado": e.estado.nombre,
            "fecha_estado_actual": e.fecha,
        }
        resultado["estaciones"][e.estacion.est_id] = estacion
    return resultado


def primer_dia_mes_actual():
    fecha = datetime.date.today().replace(day=1)
    return fecha


def dia_hoy():
    fecha = datetime.date.today()
    return fecha


def datos_precipitacion(estacion_id, inicio, fin):
    estacion = Estacion.objects.get(pk=estacion_id)
    estacion = estacion.est_codigo

    if inicio is None:
        inicio = datetime.datetime.now()
        inicio = datetime.datetime.strptime(inicio, "%Y-%m-%d")
    inicio = inicio + " " + "00:00:00"

    if fin is None:
        fin = datetime.datetime.now()
        fin = datetime.datetime.strptime(fin, "%Y-%m-%d")
    fin = fin + " " + "23:59:59"

    sql = """
    with 
    crudos as (
        select *, date(fecha) AS año_mes_dia from medicion_var1medicion 
        where estacion_id = %s and fecha >= %s and fecha <= %s
    ),
    acumulado as (
        select c.año_mes_dia, sum(c.valor) 
        from crudos c
        group by año_mes_dia
    )
    select a.año_mes_dia AS fecha, a.sum AS valor
    from acumulado a
    order by a.año_mes_dia;
    """
    consulta = PrecipitacionAcumulada.objects.raw(sql, [estacion_id, inicio, fin])

    valor = []
    fecha = []
    acumulado = []
    acumulado_valor = 0
    for fila in consulta:
        valor.append(fila.valor)
        fecha.append(fila.fecha)
        acumulado_valor = acumulado_valor + fila.valor
        acumulado.append(acumulado_valor)

    ######################################################################################
    sql2 = """
        select fecha, valor 
        from medicion_var1medicion 
        where estacion_id = %s and fecha >= %s and fecha <= %s 
        and valor > 0.0
        order by fecha;
    """
    consulta2 = PrecipitacionEventos.objects.raw(sql2, [estacion_id, inicio, fin])

    valor_mayor_a_cero = []
    for fila in consulta2:
        valor_mayor_a_cero.append(
            [fila.fecha.strftime("%Y-%d-%m %H:%M:%S"), fila.valor]
        )

    ######################################################################################
    fecha_split = fin.split("-")
    año = int(fecha_split[0])
    mes = int(fecha_split[1])

    historico = [None, None, None, None, None, None, None, None, None, None, None, None]
    historico_cuentas = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    actual = [None, None, None, None, None, None, None, None, None, None, None, None]

    sql3 = """
        select
            row_number() OVER (ORDER BY fecha) id, 
            extract(YEAR FROM fecha)::integer AS año, 
            extract(MONTH FROM fecha)::integer AS mes, 
            valor
        from mensual_var1mensual 
        where estacion_id = %s and fecha <= %s
        order by fecha asc;
    """
    consulta3 = PrecipitacionMultianual.objects.raw(sql3, [estacion_id, fin])
    ultimo_validado = None
    for fila in consulta3:
        if fila.año < año:
            if fila.valor is not None:
                if historico[fila.mes - 1] is None:
                    historico[fila.mes - 1] = fila.valor
                    historico_cuentas[fila.mes - 1] = 1
                else:
                    historico[fila.mes - 1] = historico[fila.mes - 1] + fila.valor
                    historico_cuentas[fila.mes - 1] = (
                        historico_cuentas[fila.mes - 1] + 1
                    )

        elif fila.año == año:
            if fila.mes <= mes:
                actual[fila.mes - 1] = fila.valor
            else:
                break
        else:
            break

        ultimo_validado = fila

    if (ultimo_validado.año < año) or (
        ultimo_validado.año == año and ultimo_validado.mes < mes
    ):
        if ultimo_validado.mes == 12:
            fecha_ini = datetime.datetime(ultimo_validado.año + 1, 1, 1, 0, 0, 0, 0)
        else:
            fecha_ini = datetime.datetime(
                ultimo_validado.año, ultimo_validado.mes + 1, 1, 0, 0, 0, 0
            )
        fecha_fin = fin
        sql3b = """
            with crudos as (	
                select *, date_trunc('MONTH', fecha)
                from medicion_var1medicion where estacion_id = %s
                and fecha >= %s and fecha <= %s
                order by fecha
            
            ),
            acumulado as (
                select c.date_trunc, sum(c.valor) 
                from crudos c
                group by date_trunc
            )
            select 
                row_number() OVER (ORDER BY date_trunc) AS id, 
                extract(YEAR FROM date_trunc)::integer AS año, 
                extract(MONTH FROM date_trunc)::integer AS mes, 
                sum AS valor
            from acumulado
            order by date_trunc;        
        """
        consulta3b = PrecipitacionMultianual.objects.raw(
            sql3b, [estacion_id, fecha_ini, fecha_fin]
        )
        for fila in consulta3b:
            if fila.año < año:
                if fila.valor is not None:
                    if historico[fila.mes - 1] is None:
                        historico[fila.mes - 1] = fila.valor
                        historico_cuentas[fila.mes - 1] = 1
                    else:
                        historico[fila.mes - 1] = historico[fila.mes - 1] + fila.valor
                        historico_cuentas[fila.mes - 1] = (
                            historico_cuentas[fila.mes - 1] + 1
                        )

            elif fila.año == año:
                if fila.mes <= mes:
                    actual[fila.mes - 1] = fila.valor
                else:
                    break

    for i in range(12):
        if historico_cuentas[i] > 0 and historico[i] is not None:
            historico[i] = historico[i] / historico_cuentas[i]

    ##################################################################################
    datos = {
        "valor": valor,
        "fecha": fecha,
        "acumulado": acumulado,
        "valor_mayor_a_cero": valor_mayor_a_cero,
        "historico": historico,
        "actual": actual,
        "año_actual": año,
    }

    resultado = {"estacion": estacion, "datos": datos}

    return resultado


def datos_precipitacion_multiestacion(estaciones_list, inicio, fin):
    inicio = datetime.datetime(
        year=inicio.year,
        month=inicio.month,
        day=inicio.day,
        hour=0,
        minute=0,
        second=0,
        microsecond=0,
    )

    fin = datetime.datetime(
        year=fin.year,
        month=fin.month,
        day=fin.day,
        hour=23,
        minute=59,
        second=59,
        microsecond=999999,
    )
    hoy = datetime.datetime.now()
    if fin > hoy:
        fin = hoy

    if inicio >= fin:
        inicio = hoy.replace(hour=0, minute=0, second=0, microsecond=0)

    sql = """
    WITH acumulado AS (
        select estacion_id, sum(valor) as acumulado
        from medicion_var1medicion m
        where m.estacion_id = ANY(%s) 
        and m.fecha >= %s and m.fecha <= %s
        group by m.estacion_id
    ),
    resultado AS (
        select 
            acum.estacion_id,
            (SELECT e.est_codigo AS cod_nombre FROM estacion_estacion e 
                WHERE e.est_id = acum.estacion_id) AS codnombre,
            acum.acumulado,
            (SELECT e2.est_latitud FROM estacion_estacion e2 WHERE e2.est_id = acum.estacion_id) AS latitud
            FROM acumulado acum  
    )
    SELECT r.estacion_id, r.codnombre, r.acumulado, latitud FROM resultado r ORDER BY r.latitud DESC;
    """
    consulta = None
    estaciones_list = list(map(int, estaciones_list))
    with connection.cursor() as cursor:
        cursor.execute(sql, [estaciones_list, inicio, fin])
        consulta = cursor.fetchall()
    res_estacion = []
    res_valor = []
    for e in consulta:
        res_estacion.append(e[1])
        res_valor.append(e[2])
    res = {"estacion": res_estacion, "valor": res_valor}
    return res
