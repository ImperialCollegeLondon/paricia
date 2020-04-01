# -*- coding: utf-8 -*-

from telemetria.models import ConfigVisualizar, AlarmaEstado, TeleVariables, PrecipitacionAcumulada, \
    PrecipitacionEventos, PrecipitacionMultianual, PrecipitacionAnual
from medicion.models import VientoPolar
import datetime
from django.apps import apps
from variable.models import Variable
from estacion.models import Estacion
import decimal
from django.db import connection


def consulta(estacion_id, inicio):
    config = ConfigVisualizar.objects.filter(estacion_id=estacion_id)
    variables = Variable.objects.filter(pk__in=config.values('variable_id').distinct())
    estacion = Estacion.objects.get(pk=estacion_id).est_codigo

    fechahora_actual = datetime.datetime.now()
    if inicio is None:
        inicio = fechahora_actual.replace(hour=0, minute=0, second=0, microsecond=0)
    else:
        inicio = datetime.datetime.strptime(inicio, '%Y-%m-%d')

    lista = {}
    viento = False
    for v in variables:

        ### Dirección viento o velocidad
        if v.var_id in (4, 5):
            viento = True
            continue

        Crudo = apps.get_model(app_label='medicion', model_name=v.var_modelo)
        tabla = 'medicion_' + str(v.var_modelo)
        sql = 'SELECT * FROM ' + tabla + ' WHERE estacion_id = %s AND fecha>= %s AND fecha<= %s order by fecha ASC;'
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

        datos = {'valor': valor, 'fecha': fecha}
        umbral_superior = config.get(variable_id=v.var_id).umbral_superior
        umbral_superior = float(umbral_superior) if umbral_superior else None
        umbral_inferior = config.get(variable_id=v.var_id).umbral_inferior
        umbral_inferior = float(umbral_inferior) if umbral_inferior else None

        lista[v.var_id] = {
            'estacion': estacion,
            'var_nombre': v.var_nombre,
            'var_unidad': v.uni_id.uni_sigla,
            'datos': datos,
            'umbral_superior': umbral_superior,
            'umbral_inferior': umbral_inferior,
        }
    if viento:
        sql = """
SELECT ROW_NUMBER() OVER (ORDER BY vvi.fecha) AS id, 
    vvi.fecha AS fecha, vvi.valor AS velocidad, dvi.valor AS direccion 
FROM medicion_velocidadviento vvi, medicion_direccionviento dvi
WHERE vvi.estacion_id = %s AND vvi.fecha>= %s AND vvi.fecha<= %s 
AND dvi.fecha = vvi.fecha AND dvi.estacion_id = vvi.estacion_id 
ORDER BY fecha ASC
        """
        consulta = VientoPolar.objects.raw(sql, [estacion_id, inicio, fechahora_actual])
        velocidad = []
        direccion = []
        for fila in consulta:
            velocidad.append(fila.velocidad)
            direccion.append(fila.direccion)

        datos = {'velocidad': velocidad, 'direccion': direccion}
        lista[405] = {
            'estacion': estacion,
            'var_nombre': 'Viento',
            'var_unidad': 'm/s y grados',
            'datos': datos,
            'umbral_superior': config.get(variable_id=v.var_id).umbral_superior,
            'umbral_inferior': config.get(variable_id=v.var_id).umbral_inferior,
        }
    return lista


def consulta_alarma_transmision():
    resultado = {}
    lim_inf_horas = TeleVariables.objects.get(nombre='ALAR_TRAN_LIMI_INFE').valor
    lim_sup_horas = TeleVariables.objects.get(nombre='ALAR_TRAN_LIMI_SUPE').valor
    resultado['limites'] = {'lim1': lim_inf_horas, 'lim2': lim_sup_horas}

    estaciones = AlarmaEstado.objects.filter(
        estacion_id__in=ConfigVisualizar.objects.order_by().values('estacion_id').distinct()
    ).order_by('estacion_id', '-fecha').distinct('estacion_id')
    resultado['estaciones'] = {}



    for e in estaciones:
        estacion = {
            'codigo': e.estacion.est_codigo + ' - ' + e.estacion.est_nombre,
            'latitud': e.estacion.est_latitud,
            'longitud': e.estacion.est_longitud,
            'estado': e.estado.nombre,
            'fecha_estado_actual': e.fecha
        }
        resultado['estaciones'][e.estacion.est_id] = estacion
    return resultado


def primer_dia_mes_actual():
    fecha = datetime.date.today().replace(day=1)
    return fecha


def dia_hoy():
    fecha = datetime.date.today()
    return fecha


def datos_precipitacion(estacion_id, inicio, fin):
    estacion = Estacion.objects.get(pk=estacion_id)
    estacion = estacion.est_codigo + ' - ' + estacion.est_nombre

    if inicio is None:
        inicio = datetime.datetime.now()
        inicio = datetime.datetime.strptime(inicio, '%Y-%m-%d')
    inicio = inicio + ' ' + '00:00:00'

    if fin is None:
        fin = datetime.datetime.now()
        fin = datetime.datetime.strptime(fin, '%Y-%m-%d')
    fin = fin + ' ' + '23:59:59'

    sql = """
    with 
    crudos as (
        select *, date(fecha) AS año_mes_dia from medicion_precipitacion 
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
        from medicion_precipitacion 
        where estacion_id = %s and fecha >= %s and fecha <= %s 
        and valor > 0.0
        order by fecha;
    """
    consulta2 = PrecipitacionEventos.objects.raw(sql2, [estacion_id, inicio, fin])

    valor_mayor_a_cero = []
    for fila in consulta2:
        valor_mayor_a_cero.append([fila.fecha.strftime("%Y-%d-%m %H:%M:%S"), fila.valor])

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
        from mensual_precipitacion 
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
                    historico_cuentas[fila.mes - 1] = historico_cuentas[fila.mes - 1] + 1

        elif fila.año == año:
            if fila.mes <= mes:
                actual[fila.mes - 1] = fila.valor
            else:
                break
        else:
            break

        ultimo_validado = fila

    if (ultimo_validado.año < año) or (ultimo_validado.año == año and ultimo_validado.mes < mes):
        if ultimo_validado.mes == 12:
            fecha_ini = datetime.datetime(ultimo_validado.año + 1, 1, 1, 0, 0, 0, 0)
        else:
            fecha_ini = datetime.datetime(ultimo_validado.año, ultimo_validado.mes + 1, 1, 0, 0, 0, 0)
        fecha_fin = fin
        sql3b = """
            with crudos as (	
                select *, date_trunc('MONTH', fecha)
                from medicion_precipitacion where estacion_id = %s
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
        consulta3b = PrecipitacionMultianual.objects.raw(sql3b, [estacion_id, fecha_ini, fecha_fin])
        for fila in consulta3b:
            if fila.año < año:
                if fila.valor is not None:
                    if historico[fila.mes - 1] is None:
                        historico[fila.mes - 1] = fila.valor
                        historico_cuentas[fila.mes - 1] = 1
                    else:
                        historico[fila.mes - 1] = historico[fila.mes - 1] + fila.valor
                        historico_cuentas[fila.mes - 1] = historico_cuentas[fila.mes - 1] + 1

            elif fila.año == año:
                if fila.mes <= mes:
                    actual[fila.mes - 1] = fila.valor
                else:
                    break

    for i in range(12):
        if historico_cuentas[i] > 0 and historico[i] is not None:
            historico[i] = historico[i] / historico_cuentas[i]

    ##################################################################################
    datos = {'valor': valor, 'fecha': fecha,
             'acumulado': acumulado, 'valor_mayor_a_cero': valor_mayor_a_cero,
             'historico': historico, 'actual': actual, 'año_actual': año}

    resultado = {
        'estacion': estacion,
        'datos': datos
    }

    return resultado


def datos_precipitacion_multiestacion(estaciones_list, inicio, fin):
    inicio = inicio.split('-')
    inicio = datetime.datetime(year=int(inicio[0]), month=int(inicio[1]), day=int(inicio[2]),
                               hour=0, minute=0, second=0, microsecond=0)
    fin = fin.split('-')
    fin = datetime.datetime(year=int(fin[0]), month=int(fin[1]), day=int(fin[2]),
                            hour=23, minute=59, second=59, microsecond=999999)
    hoy = datetime.datetime.now()
    if fin > hoy:
        fin = hoy

    if inicio >= fin:
        inicio = hoy.replace(hour=0, minute=0, second=0, microsecond=0)

    sql = """
    WITH acumulado AS (
        select estacion_id, sum(valor) as acumulado
        from medicion_precipitacion m
        where m.estacion_id = ANY(%s) 
        and m.fecha >= %s and m.fecha <= %s
        group by m.estacion_id
    ),
    resultado AS (
        select 
            acum.estacion_id,
            (SELECT e.est_codigo || ' - ' || e.est_nombre AS cod_nombre FROM estacion_estacion e 
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
    res = {'estacion': res_estacion, 'valor': res_valor}
    return res
