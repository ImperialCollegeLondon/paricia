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

import pandas as pd
from django.apps import apps
from django.db import connection

from estacion.models import Estacion
from frecuencia.models import Frecuencia
from home.functions import objdict
from variable.models import Variable

_model = {
    "Subhorario crudo": objdict({"app": "medicion", "model": "medicion"}),
    "Subhorario validado": objdict({"app": "validacion", "model": "Validado"}),
    "Horario": objdict({"app": "horario", "model": "horario"}),
    "Diario": objdict({"app": "diario", "model": "diario"}),
    "Mensual": objdict({"app": "mensual", "model": "mensual"}),
}


def datos_grafico1(estacion_id, variables_id, profundidad, inicio, fin):
    variables = Variable.objects.filter(pk__in=variables_id)
    estacion = Estacion.objects.get(pk=estacion_id)
    estacion = estacion.est_codigo

    if inicio is None:
        inicio = datetime.datetime.now()
        inicio = datetime.datetime.strptime(inicio, "%Y-%m-%d")
    inicio = inicio + " " + "00:00:00"

    if inicio is None:
        inicio = datetime.datetime.now()
        inicio = datetime.datetime.strptime(inicio, "%Y-%m-%d")
    fin = fin + " " + "23:59:59"

    lista = {}
    for v in variables:
        Crudo = apps.get_model(
            app_label="medicion", model_name="Var" + str(v.var_id) + "Medicion"
        )
        tabla = "validacion_var" + str(v.var_id) + "validado"
        sql = (
            "SELECT * FROM "
            + tabla
            + " WHERE estacion_id = %s AND profundidad = %s AND fecha>= %s AND fecha<= %s order by fecha ASC;"
        )
        consulta = Crudo.objects.raw(sql, [estacion_id, profundidad, inicio, fin])

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
            # TODO:  cambiar por el valor de frecuencia ingresada al sistema
            if diff_dt.seconds > 3609 or diff_dt.days > 0:
                valor.append(None)
                fecha.append(fecha_anterior + datetime.timedelta(minutes=60))
            valor.append(fila.valor)
            fecha.append(fila.fecha)
            fecha_anterior = fila.fecha

        datos = {"valor": valor, "fecha": fecha}

        lista[v.var_id] = {
            "estacion": estacion,
            "var_nombre": v.var_nombre,
            "var_codigo": v.var_codigo,
            "var_unidad": v.uni_id.uni_sigla,
            "datos": datos,
        }

    return lista


def datos_crudos_grafico1(estacion_id, variables_id, profundidad, inicio, fin):
    variables = Variable.objects.filter(pk__in=variables_id)
    estacion = Estacion.objects.get(pk=estacion_id)
    estacion = estacion.est_codigo

    if inicio is None:
        inicio = datetime.datetime.now()
        inicio = datetime.datetime.strptime(inicio, "%Y-%m-%d")
    inicio = inicio + " " + "00:00:00"

    if inicio is None:
        inicio = datetime.datetime.now()
        inicio = datetime.datetime.strptime(inicio, "%Y-%m-%d")
    fin = fin + " " + "23:59:59"

    lista = {}
    for v in variables:
        Crudo = apps.get_model(
            app_label="medicion", model_name="Var" + str(v.var_id) + "Medicion"
        )
        tabla = "medicion_var" + str(v.var_id) + "medicion"
        sql = (
            "SELECT * FROM "
            + tabla
            + " WHERE estacion_id = %s AND profundidad = %s AND fecha>= %s AND fecha<= %s order by fecha ASC;"
        )
        consulta = Crudo.objects.raw(sql, [estacion_id, profundidad, inicio, fin])

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
            # TODO:  cambiar por el valor de frecuencia ingresada al sistema
            if diff_dt.seconds > 3609 or diff_dt.days > 0:
                valor.append(None)
                fecha.append(fecha_anterior + datetime.timedelta(minutes=60))
            valor.append(fila.valor)
            fecha.append(fila.fecha)
            fecha_anterior = fila.fecha

        datos = {"valor": valor, "fecha": fecha}

        lista[v.var_id] = {
            "estacion": estacion,
            "var_nombre": v.var_nombre,
            "var_codigo": v.var_codigo,
            "var_unidad": v.uni_id.uni_sigla,
            "datos": datos,
        }

    return lista


def datos_grafico2(estacion_id, variables_id, profundidad, inicio, fin):
    variables = Variable.objects.filter(pk__in=variables_id)
    estacion = Estacion.objects.get(pk=estacion_id)
    estacion = estacion.est_codigo

    if inicio is None:
        inicio = datetime.datetime.now()
        inicio = datetime.datetime.strptime(inicio, "%Y-%m-%d")
    inicio = inicio + " " + "00:00:00"

    if inicio is None:
        inicio = datetime.datetime.now()
        inicio = datetime.datetime.strptime(inicio, "%Y-%m-%d")
    fin = fin + " " + "23:59:59"

    lista = {}
    for v in variables:
        tabla = "validacion_var" + str(v.var_id) + "validado"
        sql = (
            "SELECT fecha, valor FROM "
            + tabla
            + " WHERE estacion_id = %s AND profundidad = %s AND fecha>= %s AND fecha<= %s order by fecha ASC;"
        )
        tabla = pd.DataFrame()
        with connection.cursor() as cursor:
            cursor.execute(sql, [estacion_id, profundidad, inicio, fin])
            resultado = cursor.fetchall()
            tabla = pd.DataFrame(resultado, columns=["fecha", "valor"])
            tabla.valor = tabla.valor.astype(float)
            tabla["hora"] = pd.DatetimeIndex(tabla["fecha"]).hour
            promedios = tabla.groupby("hora")["valor"].mean()

        valor = []
        hora = []
        for _hora, _valor in promedios.iteritems():
            hora.append(_hora)
            valor.append(_valor)

        datos = {"valor": valor, "hora": hora}

        lista[v.var_id] = {
            "estacion": estacion,
            "var_nombre": v.var_nombre,
            "var_codigo": v.var_codigo,
            "var_unidad": v.uni_id.uni_sigla,
            "datos": datos,
        }

    return lista


def datos_comparar_hidro(
    fre, _inicio, _fin, est_calidad, profundidad, var_calidad, est_hidro, var_hidro
):
    inicio = datetime.datetime.strftime(_inicio, "%Y-%m-%d")
    inicio = inicio + " " + "00:00:00"
    inicio_datetime = datetime.datetime.strptime(inicio, "%Y-%m-%d %H:%M:%S")
    fin = datetime.datetime.strftime(_fin, "%Y-%m-%d")
    fin = fin + " " + "23:59:59"
    fin_datetime = datetime.datetime.strptime(fin, "%Y-%m-%d %H:%M:%S")

    freq_calidad = Frecuencia.objects.filter(est_id=est_calidad)
    freq_hidro = Frecuencia.objects.filter(est_id=est_hidro)

    lista = {}
    lista["est_calidad"] = {
        "codigo": est_calidad.est_codigo,
        "nombre": est_calidad.est_nombre,
    }
    lista["est_hidro"] = {
        "codigo": est_hidro.est_codigo,
        "nombre": est_hidro.est_nombre,
    }

    lista_calidad = {}
    for v in var_calidad:
        Datos = apps.get_model(
            app_label=_model[fre.nombre].app,
            model_name="Var" + str(v) + _model[fre.nombre].model.capitalize(),
        )
        tabla = (
            _model[fre.nombre].app + "_var" + str(v) + _model[fre.nombre].model.lower()
        )
        sql = "SELECT * FROM " + tabla + " WHERE estacion_id = %s AND profundidad = %s "
        sql += (
            "AND fecha>= %s AND fecha<= %s  AND valor IS NOT NULL ORDER BY fecha ASC;"
        )
        consulta = Datos.objects.raw(
            sql, [est_calidad.est_id, profundidad, inicio, fin]
        )

        valor = []
        fecha = []
        fecha_anterior = None

        frecuencias = None
        intervalo_frecuencia = None
        frec_segundos = None

        frecuencias = (
            freq_calidad.filter(var_id=v)
            .order_by("fre_fecha_ini")
            .values_list("fre_fecha_ini", "fre_valor", named=True)
        )
        frecuencias = construir_intervalos_freq(
            frecuencias, inicio_datetime, fin_datetime
        )
        intervalo_frecuencia = frecuencias.pop()
        frec_segundos = intervalo_frecuencia["freq"] * 60

        for fila in consulta:
            if fecha_anterior is None:
                valor.append(fila.valor)
                fecha.append(fila.fecha)
                fecha_anterior = fila.fecha
                continue

            diff_dt = fila.fecha - fecha_anterior
            while not (
                intervalo_frecuencia["inicio"]
                <= fila.fecha
                < intervalo_frecuencia["fin"]
            ):
                intervalo_frecuencia = frecuencias.pop()
                frec_segundos = intervalo_frecuencia["freq"] * 60

            if diff_dt.seconds > (frec_segundos + 40) or diff_dt.days > 0:
                valor.append(None)
                fecha.append(
                    fecha_anterior + datetime.timedelta(minutes=int(frec_segundos / 60))
                )
            valor.append(fila.valor)
            fecha.append(fila.fecha)
            fecha_anterior = fila.fecha

        datos = {"valor": valor, "fecha": fecha}

        variable = Variable.objects.get(pk=v)
        lista_calidad[v] = {
            "var_nombre": variable.var_nombre,
            "var_codigo": variable.var_codigo,
            "var_unidad": variable.uni_id.uni_sigla,
            "var_es_acumulada": variable.es_acumulada,
            "datos": datos,
        }
    lista["calidad"] = lista_calidad

    lista_hidro = {}
    for v in var_hidro:
        Datos = apps.get_model(
            app_label=_model[fre.nombre].app,
            model_name="Var" + str(v) + _model[fre.nombre].model.capitalize(),
        )
        tabla = (
            _model[fre.nombre].app + "_var" + str(v) + _model[fre.nombre].model.lower()
        )
        sql = (
            "SELECT * FROM "
            + tabla
            + " WHERE estacion_id = %s AND fecha>= %s AND fecha<= %s "
        )
        sql += " AND valor IS NOT NULL ORDER BY fecha ASC;"
        consulta = Datos.objects.raw(sql, [est_hidro.est_id, inicio, fin])

        valor = []
        fecha = []
        fecha_anterior = None

        frecuencias = None
        intervalo_frecuencia = None
        frec_segundos = None

        frecuencias = (
            freq_hidro.filter(var_id=v)
            .order_by("fre_fecha_ini")
            .values_list("fre_fecha_ini", "fre_valor", named=True)
        )
        frecuencias = construir_intervalos_freq(
            frecuencias, inicio_datetime, fin_datetime
        )
        intervalo_frecuencia = frecuencias.pop()
        frec_segundos = intervalo_frecuencia["freq"] * 60

        for fila in consulta:
            if fecha_anterior is None:
                valor.append(fila.valor)
                fecha.append(fila.fecha)
                fecha_anterior = fila.fecha
                continue

            diff_dt = fila.fecha - fecha_anterior

            while not (
                intervalo_frecuencia["inicio"]
                <= fila.fecha
                < intervalo_frecuencia["fin"]
            ):
                intervalo_frecuencia = frecuencias.pop()
                frec_segundos = intervalo_frecuencia["freq"] * 60

            if diff_dt.seconds > (frec_segundos + 40) or diff_dt.days > 0:
                valor.append(None)
                fecha.append(
                    fecha_anterior + datetime.timedelta(minutes=int(frec_segundos / 60))
                )
            valor.append(fila.valor)
            fecha.append(fila.fecha)
            fecha_anterior = fila.fecha

        datos = {"valor": valor, "fecha": fecha}

        variable = Variable.objects.get(pk=v)
        lista_hidro[v] = {
            "var_nombre": variable.var_nombre,
            "var_codigo": variable.var_codigo,
            "var_unidad": variable.uni_id.uni_sigla,
            "var_es_acumulada": variable.es_acumulada,
            "datos": datos,
        }
    lista["hidro"] = lista_hidro
    return lista


def construir_intervalos_freq(freqs, inicio, fin):
    rangos = []

    try:
        if inicio < freqs[0].fre_fecha_ini:
            return rangos
    except:
        return rangos

    for i in reversed(range(len(freqs))):
        if i == len(freqs) - 1:
            rangos.append(
                {
                    "inicio": freqs[i].fre_fecha_ini,
                    "fin": datetime.datetime.now(),
                    "freq": freqs[i].fre_valor,
                }
            )
            continue
        #######################################
        if freqs[i + 1].fre_fecha_ini >= inicio:
            #######################################
            if inicio < freqs[i + 1].fre_fecha_ini:
                rangos.append(
                    {
                        "inicio": freqs[i].fre_fecha_ini,
                        "fin": freqs[i + 1].fre_fecha_ini,
                        "freq": freqs[i].fre_valor,
                    }
                )
    return rangos
