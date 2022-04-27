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

"""These functions are used in the views to calculate various hydrological indices. 
"""

import decimal
import json

# import frecuencia.models as freq
# from anuarios.models import Var1Anuarios
from datetime import datetime, timedelta
from decimal import Decimal

import numpy as np
import pandas as pd
from django.core import serializers
from django.db import connection
from django.db.models import Avg, Count, Max, Min, Sum

import anual.models as anio
import diario.models as dia
import horario.models as hora
import mensual.models as mes
import validacion.models as vali
from estacion.models import Estacion

# from anuarios import anuario
from variable.models import Variable

dict_mes = {
    1: "Ene",
    2: "Feb",
    3: "Mar",
    4: "Abr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Ago",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dic",
}


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return {"__Decimal__": str(obj)}
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)


class DateTimeEncoder(json.JSONEncoder):
    # Override the default method
    def default(self, obj):
        if isinstance(obj, (datetime.date, datetime.datetime)):
            return {obj.strftime("%m/%d/%Y")}
        return json.JSONEncoder.default(self, obj)


def periodos(i):
    switcher = {
        0: "validado",
        1: "diario",
        2: "horario",
        3: "mensual",
    }
    return switcher.get(i, "valor invalido")


# retorna la lista de datos validado, dado el id de variable, la estacion, fecha inicio y fecha fin
def getVarValidado(varid, estacion_id, inicio, fin, frecuencia):
    """Returns the list of validated data, given the variable id,
    the station, start date and end date.
    """
    try:
        var = Variable.objects.get(var_id__exact=varid)
        tabla = var.var_codigo  # varcodigo
    except Variable.DoesNotExist:
        var = None

    print("frecuencia desde el view", frecuencia)
    # print(globals())
    if var is not None and estacion_id is not None:
        # print("desde el metodo validacion.functions.getVarValidado")
        if frecuencia == 0:
            print(
                "Fecha inicio "
                + inicio.strftime("%m-%d-%Y %H:%M:%S")
                + " fecha fin "
                + fin.strftime("%m-%d-%Y %H:%M:%S")
            )
            print("Estacion id " + str(estacion_id))
            sql = (
                "WITH seleccion AS ("
                "SELECT id, fecha, valor, validacion FROM validacion_"
                + tabla.lower()
                + " WHERE estacion_id = "
                + str(estacion_id)
                + " and fecha >= '"
                + inicio.strftime("%d-%m-%Y %H:%M:%S")
                + "' and fecha <= '"
                + fin.strftime("%d-%m-%Y %H:%M:%S")
                + "'"
                ") SELECT ss.id, ss.fecha, ss.valor FROM ("
                "SELECT fecha, MAX(validacion) AS validacion FROM seleccion GROUP BY fecha "
                ") AS tbl_max "
                "INNER JOIN seleccion ss ON ss.fecha = tbl_max.fecha "
                "AND ss.validacion = tbl_max.validacion ORDER BY ss.fecha;"
            )
            # print(sql)
            return vali.Var1Validado.objects.raw(sql)
        elif frecuencia == 1:  # 'Horario':
            print("entra en horarios")
            return hora.Var1Horario.objects.filter(
                estacion_id__exact=estacion_id, fecha__gte=inicio, fecha__lte=fin
            ).values("id", "fecha", "valor")
        elif frecuencia == 2:  # 'Diario':
            return dia.Var1Diario.objects.filter(
                estacion_id__exact=estacion_id, fecha__gte=inicio, fecha__lte=fin
            ).values("id", "fecha", "valor")
        else:  # 'Mensual':
            print("entra en mensuales")
            return mes.Var1Mensual.objects.filter(
                estacion_id__exact=estacion_id, fecha__gte=inicio, fecha__lte=fin
            ).values("id", "fecha", "valor")
    else:
        return None


# Doblemasa
def acumularDoble(est1, est2, frecuencia):
    """Used in DoubleMass calculation in views."""

    # print("metodo acumular")
    data = []
    """ fechas = []
    valor = [] """
    acume1 = 0
    acume2 = 0
    acumTme1 = 0
    acumTme2 = 0
    # print("entra en el else")
    # print("Imprimiendo datos ")
    for d1 in zip(est1, est2):
        # print(d1[0]['valor'])
        if frecuencia == 0:
            acumTme1 = d1[0].valor
            acume1 = acume1 + acumTme1
            acumTme2 = d1[1].valor
            acume2 = acume2 + acumTme2
            dic = {
                "fecha": d1[0].fecha.strftime("%m/%d/%Y %H:%M:%S"),
                "valore1": str(d1[0].valor),
                "acume1": str(acume1),
                "valore2": str(d1[1].valor),
                "acume2": str(acume2),
            }
            # dic = {'fecha': d1[0].fecha.strftime("%m/%d/%Y %H:%M:%S"), 'valore1': d1[0].valor,
            #        'acume1': acume1, "valore2": d1[1].valor, "acume2": acume2}
        else:
            acumTme1 = d1[0]["valor"]
            acume1 = acume1 + acumTme1
            acumTme2 = d1[1]["valor"]
            acume2 = acume2 + acumTme2
            dic = {
                "fecha": d1[0]["fecha"].strftime("%Y%m/%d/%Y %H:%M:%S"),
                "valore1": str(d1[0]["valor"]),
                "acume1": str(acume1),
                "valore2": str(d1[1]["valor"]),
                "acume2": str(acume2),
            }
        data.append(dic)

    return data


# doblemasa
def consultaPeriodos(estacion_id, frecuencia):
    """Used in views.DoubleMass calculation to get max and min dates for period."""
    fmax = None
    fmin = None
    estacion = None

    if frecuencia == 0:
        fmax = (
            vali.Var1Validado.objects.filter(estacion_id__exact=estacion_id)
            .order_by("fecha")
            .values("fecha")[:1]
        )
        fmin = (
            vali.Var1Validado.objects.filter(estacion_id__exact=estacion_id)
            .order_by("-fecha")
            .values("fecha")[:1]
        )
    elif frecuencia == 1:  # 'Horario':
        fmax = (
            hora.Var1Horario.objects.filter(estacion_id__exact=estacion_id)
            .order_by("fecha")
            .values("fecha")[:1]
        )
        fmin = (
            hora.Var1Horario.objects.filter(estacion_id__exact=estacion_id)
            .order_by("-fecha")
            .values("fecha")[:1]
        )
    elif frecuencia == 2:  # 'Diario':
        fmax = (
            dia.Var1Diario.objects.filter(estacion_id__exact=estacion_id)
            .order_by("fecha")
            .values("fecha")[:1]
        )
        fmin = (
            dia.Var1Diario.objects.filter(estacion_id__exact=estacion_id)
            .order_by("-fecha")
            .values("fecha")[:1]
        )
    else:  # 'Mensual':
        fmax = (
            mes.Var1Mensual.objects.filter(estacion_id__exact=estacion_id)
            .order_by("fecha")
            .values("fecha")[:1]
        )
        fmin = (
            mes.Var1Mensual.objects.filter(estacion_id__exact=estacion_id)
            .order_by("-fecha")
            .values("fecha")[:1]
        )
    estacion = Estacion.objects.filter(est_id__exact=estacion_id).values(
        "est_codigo", "est_nombre"
    )[:1]

    return fmax, fmin, estacion


from time import time


def intensidadDiracion(estacion_id, fechaini, fechafin):
    """Used to calculate the intensity-duration index."""
    tiempo_inicial = time()
    periodos = [5, 10, 15, 30, 60, 120, 1440, 2880]
    # print(estacion_id, fechaini, fechafin)
    est = Estacion.objects.get(pk=estacion_id)
    c = connection.cursor()
    fechas = []
    valores = []
    intensidad = []
    intervalos = []
    try:
        for p in periodos:
            c.execute("BEGIN")
            c.callproc("acumular", (estacion_id, fechaini, fechafin, p))
            result = c.fetchall()
            # print("result ",result)
            cad = result[0][0].split(";")
            maximo = float(cad[1])
            if maximo >= 0:
                fechas.append(cad[0])
                valores.append(maximo)
                intensidad.append(round(maximo / (p / 60), 1))
                intervalos.append(p)
        c.close()
    finally:
        c.close()
    if len(fechas) == 0:
        mensaje = (
            "No hay datos para procesar en la estacion "
            + str(est.est_codigo)
            + " en el año selecionado"
        )
    else:
        mensaje = "los cálculos se realizaron con éxito"

    tiempo_final = time()
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print("ejecutado en ", tiempo_ejecucion)
    datadict = {
        "estacion_id": est.est_codigo,
        "fecha": fechas,
        "maximo": valores,
        "inte": intensidad,
        "iterval": intervalos,
        "mensaje": mensaje,
    }
    # print(datadict)
    return datadict


#### calcula los datos para la curva de duracion sin la influencia de la estacion
def getCaudalFrec(estacion_id, inicio, fin, frecuencia):
    """Calculate the specific flow of a hydrological station. Used to calculate
    the duration flow index."""

    est = Estacion.objects.get(est_id=estacion_id)
    inf = est.influencia_km
    print(
        estacion_id,
        "influencia ",
        inf,
        "fecha ini :",
        inicio.year,
        type(inicio),
        " fecha fin: ",
        fin.year,
    )
    anios = []
    totaldf = pd.DataFrame()
    ainf = False
    long = 0
    if inf is None:
        div = 1
    elif inf > 0:
        div = inf
        ainf = True
    else:
        div = 1
    listanual = {}
    for anio in range(inicio.year, fin.year + 1):
        print("procesar año ", anio, "valor del div", div, "ainf ", ainf)
        caudal = getCaudalanio(frecuencia, estacion_id, anio)
        if caudal is not None and len(caudal) > 30:
            anios.append(anio)
            if len(caudal) > long:
                long = len(caudal)
            df = pd.DataFrame(caudal)
            totaldf = pd.concat([totaldf, df])
            df["CauEsp"] = df["valor"] / div
            df["CauEsp"] = round(df["CauEsp"].astype(float), 3)
            df = df.sort_values(by=["valor"], ascending=[True])
            td = len(df["valor"])
            df["valor"] = round(df["valor"].astype(float), 3)
            df["rango"] = range(1, td + 1)
            df["frecuencia"] = round((df["rango"] / td) * 1, 9)
            df["valor"] = df["valor"].values[::-1]
            df["CauEsp"] = df["CauEsp"].values[::-1]
            listanual["cau" + str(anio)] = df["valor"].fillna("null").tolist()
            listanual["cauEsp" + str(anio)] = df["CauEsp"].fillna("null").tolist()
            listanual["fre" + str(anio)] = df["frecuencia"].fillna("null").tolist()
    if len(totaldf) > 30:
        totaldf["CauEsp"] = totaldf["valor"] / div
        totaldf["CauEsp"] = round(totaldf["CauEsp"].astype(float), 3)
        totaldf = totaldf.sort_values(by=["valor"], ascending=[True])
        td = len(totaldf["valor"])
        totaldf["valor"] = round(totaldf["valor"].astype(float), 2)
        totaldf["rango"] = range(1, td + 1)
        totaldf["frecuencia"] = round((totaldf["rango"] / td) * 1, 9)
        totaldf["valor"] = totaldf["valor"].values[::-1]
        totaldf["CauEsp"] = totaldf["CauEsp"].values[::-1]
        totdic = {
            "cau": totaldf["valor"].fillna("null").tolist(),
            "cauEsp": totaldf["CauEsp"].fillna("null").tolist(),
            "fre": totaldf["frecuencia"].fillna("null").tolist(),
        }
        dian = {
            "mayor": long,
            "aporte": ainf,
            "anios": anios,
            "anuales": listanual,
            "total": totdic,
        }
    else:
        dian = None
    return dian
    # return json.dumps(dian, allow_nan=True,cls=DecimalEncoder)


def getCaudalanio(frecuencia, estacion_id, anio):
    """Get flow for a specific year at a specific station."""
    # print("frecuencia", "estacion_id","anio")
    # print('   ',frecuencia,"   ", estacion_id,"   ","    ",anio)
    fi = str(anio) + "-01-01"
    ff = str(anio) + "-12-31"
    inicio = datetime.strptime(fi, "%Y-%m-%d")
    fin = datetime.strptime(ff, "%Y-%m-%d")
    if frecuencia == 1:  # 'Horario':
        # print("entra en horario frecuencia ", frecuencia, estacion_id, inicio)
        hq = hora.Var10Horario.objects.filter(
            estacion_id__exact=estacion_id,
            fecha__gte=inicio,
            fecha__lte=fin,
            valor__isnull=False,
        ).values(
            "valor"
        )  # Cambiar aki
        # print(hq.query)
        return hq
    if frecuencia == 2:  # 'Diario':
        # print("entra en diario ",frecuencia)
        dq = dia.Var10Diario.objects.filter(
            estacion_id__exact=estacion_id,
            fecha__gte=inicio,
            fecha__lte=fin,
            valor__isnull=False,
        ).values(
            "valor"
        )  # Cambiar aki
        # print(dq.query)
        return dq
    return None


def getCaudalFrecMulti(listEst, fin, ffi):
    """Calculate the flow at multiple hydrological stations. Used to calculate
    the duration flow index.
    """
    print("getCaudalFrecMulti:")
    if len(listEst) > 0:
        estaciones = []
        calculos = {}
        codigos = []
        for est in listEst:
            print(est)
            esta = Estacion.objects.get(est_id=est)
            inf = esta.influencia_km
            if inf is None:
                div = 1
            elif inf > 0:
                div = inf
            else:
                div = 1
            dq = (
                dia.Var10Diario.objects.filter(
                    estacion_id__exact=est,
                    fecha__gte=fin,
                    fecha__lte=ffi,
                    valor__isnull=False,
                )
                .values("valor", "fecha")
                .order_by("fecha")
            )

            if dq is not None and len(dq) > 30:
                df = pd.DataFrame(dq)
                # print(df.head(10))
                codigos.append(est)
                df["CauEsp"] = df["valor"] / div
                df["CauEsp"] = round(df["CauEsp"].astype(float), 3)
                df = df.sort_values(by=["valor"], ascending=[True])
                td = len(df["valor"])
                df["valor"] = round(df["valor"].astype(float), 2)
                df["rango"] = range(1, td + 1)
                df["frecuencia"] = round((df["rango"] / td) * 1, 9)
                df["valor"] = df["valor"].values[::-1]
                df["CauEsp"] = df["CauEsp"].values[::-1]
                calculos["cau" + str(est)] = df["valor"].fillna("null").tolist()
                calculos["cauEsp" + str(est)] = df["CauEsp"].fillna("null").tolist()
                calculos["fre" + str(est)] = df["frecuencia"].fillna("null").tolist()
                print(
                    "fecha inicio ",
                    df["fecha"][0],
                    "fecha fin ",
                    df["fecha"][len(df) - 1],
                )
                estaciones.append(
                    {
                        "estacion": esta.est_codigo,
                        "inicio": df["fecha"][0].strftime("%d/%m/%Y"),
                        "fin": df["fecha"][len(df) - 1].strftime("%d/%m/%Y"),
                    }
                )
        # print(calculos)
        dict = {"estaciones": estaciones, "codigos": codigos, "datos": calculos}
        return json.dumps(dict, allow_nan=True, cls=DecimalEncoder)
    else:
        return None


"""Esta clase se encarga de calcular los indicadores de precipitación,
Cada funcion de la clase calcula un indicador determinado"""


class IndicadoresPrecipitacion:
    """This class is responsible for calculating precipitation indicators,
    each method of the class calculates a certain indicator.
    """

    def __init__(self, estacion_id, inicio, fin, completo):
        self.estacion = estacion_id
        self.inicio = inicio
        self.fin = fin + timedelta(hours=23, minutes=59, seconds=59)
        self.completo = completo
        variable = Variable.objects.get(pk=1)
        self.vacios = variable.vacios

    def rr_anual(self):
        print(self.inicio, self.fin)
        """precipitacion media anual precipitacion promedio del rango de fechas seleccionada.
        average annual precipitation average precipitation of the selected date range.
        """
        rranual = anio.Var1Anual.objects.filter(
            estacion_id__exact=self.estacion,
            fecha__gte=self.inicio,
            fecha__lte=self.fin,
            valor__isnull=False,
            vacios__lt=self.vacios,
        ).order_by("fecha")

        if rranual is not None:
            return rranual
        else:
            return None

    def rr_mensual(self):
        """devuelve la tabla de datos mensuales para la fecha seleccionadas.
        returns the monthly data table for the selected date.
        """
        rrmensual = mes.Var1Mensual.objects.filter(
            estacion_id__exact=self.estacion,
            fecha__gte=self.inicio,
            fecha__lte=self.fin,
            vacios__lt=self.vacios,
        ).order_by("fecha")
        if rrmensual is not None:
            return rrmensual
        else:
            return None

    def rr_max_hora(self):
        """calcula la precipitacion maxima acumulada en 24 horas.
        calculates the maximum accumulated precipitation in 24 hours.
        """
        datos = (
            vali.Var1Validado.objects.filter(
                estacion_id__exact=self.estacion,
                fecha__gte=self.inicio,
                fecha__lte=self.fin,
                valor__isnull=False,
            )
            .order_by("fecha")
            .values("fecha", "valor")
        )
        df = pd.DataFrame.from_records(datos)
        df["valor"] = pd.to_numeric(df["valor"])
        minutos_inicio = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
        maximos = []
        fechas = []
        for i in minutos_inicio:
            df["offset"] = df["fecha"] - timedelta(minutes=i)
            df2 = df[df["offset"] >= self.inicio]
            df2["offset"] = df["offset"].dt.floor("h")
            dfr = df2.groupby("offset").agg({"valor": "sum"})
            idx = dfr["valor"].idxmax()
            val = dfr["valor"][idx]
            maximos.append(val)
            fechas.append(idx)
        maximo = max(maximos)
        max_idx = maximos.index(maximo)
        offset = minutos_inicio[max_idx]
        fecha_ini = fechas[max_idx] + timedelta(minutes=offset) - timedelta(minutes=5)
        fecha_fin = fecha_ini + timedelta(hours=1)
        return {
            "valor_max": maximo,
            "fecha_ini": fecha_ini.strftime("%Y/%m/%d %H:%M:%S"),
            "fecha_fin": fecha_fin.strftime("%Y/%m/%d %H:%M:%S"),
        }

    def percentilesDiarios(self):
        """Calcula los percentelies en base a los datos diarios.
        Calculate percentelies based on daily data.
        """
        diarios = list(
            dia.Var1Diario.objects.filter(
                estacion_id__exact=self.estacion,
                fecha__gte=self.inicio,
                fecha__lte=self.fin,
                valor__isnull=False,
                valor__gt=0,
                vacios__lt=self.vacios,
            ).values_list("valor")
        )
        # print("typo de datos en percentiles ", type(diarios))
        # print(diarios)
        a = np.array(diarios, dtype=object)
        q10 = round(np.percentile(a, 10, interpolation="lower"), 1)
        q95 = round(np.percentile(a, 95, interpolation="lower"), 1)
        return {"q10": q10, "q95": q95}

    def percentilesHorarios(self):
        """Calcula los percentelies en base a los horarios.
        Calculates hourly percentiles."""
        horarios = list(
            hora.Var1Horario.objects.filter(
                estacion_id__exact=self.estacion,
                fecha__gte=self.inicio,
                fecha__lte=self.fin,
                valor__isnull=False,
                valor__gt=0,
                vacios__lt=self.vacios,
            ).values_list("valor")
        )
        a = np.array(horarios, dtype=object)
        q10 = round(np.percentile(a, 10, interpolation="lower"), 1)
        q95 = round(np.percentile(a, 95, interpolation="lower"), 1)
        return {"q10": q10, "q95": q95}

    def calcular_dias_sin_precipitacion(self):
        """Calculates days without precipitation."""
        sql = """
        SELECT COUNT(*) FROM diario_var1diario 
        WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s AND valor = 0.0
            AND vacios < %s;
        """
        with connection.cursor() as cursor:
            cursor.execute(sql, [self.estacion, self.inicio, self.fin, self.vacios])
            resultado = cursor.fetchall()
        return resultado[0][0]

    def makeDic(self):
        """HELPWANTED: What does this do?"""
        anuales = self.rr_anual()
        # print(anuales)

        anioSecoMin = 1000000
        anioHumedoMax = 0
        iter = 0
        fechaMin = None
        fechaMax = None
        promedio = 0
        # print("años consultados ",anuales.count())
        if anuales.count() == 0:
            return None

        for an in anuales:  # controla que el año tenga mas de 11 meses
            # print("fecha anual =>  ",an.fecha, "valor", an.valor," completoHumbral ",an.completo_umbral)
            # mescontado = mes.Precipitacion.objects.filter(estacion_id__exact = self.estacion,fecha__gte=self.inicio,
            #                                        fecha__lte = self.fin, valor__isnull=False)

            if an.vacios < self.vacios:
                promedio += an.valor
                if an.valor < anioSecoMin:
                    anioSecoMin = an.valor
                    fechaMin = an.fecha
                if an.valor > anioHumedoMax:
                    anioHumedoMax = an.valor
                    fechaMax = an.fecha
                iter += 1
            # print("promedio ",promedio)

        if promedio > 0:
            promedio = str(round((promedio / iter), 1))
            secHum = {
                "anio_seco": str(round(anioSecoMin, 1)),
                "fechsec": fechaMin.strftime("%Y"),
                "anio_humedo": str(round(anioHumedoMax, 1)),
                "fechhum": fechaMax.strftime("%Y"),
            }
        else:
            promedio = "S/D"
            secHum = {
                "anio_seco": "S/D",
                "fechsec": "S/D",
                "anio_humedo": "S/D",
                "fechhum": "S/D",
            }

        max_hora = self.rr_max_hora()

        mensuales = self.rr_mensual()
        percentiles_horarios = self.percentilesHorarios()
        percentiles_diarios = self.percentilesDiarios()

        # print("****************************dict *******************")
        anual2json = serializers.serialize(
            "json",
            anuales,
            fields=(
                "fecha",
                "valor",
                "vacios",
                "dias_con_lluvia",
                "dias_sin_lluvia",
                "mes_lluvioso",
                "mes_seco",
                "mes_lluvioso_valor",
                "mes_seco_valor",
                "estacionalidad",
            ),
        )
        anuales = json.loads(anual2json)
        mes2json = serializers.serialize("json", mensuales, fields=("fecha", "valor"))
        mensuales = json.loads(mes2json)
        dias_sin_precipitacion = self.calcular_dias_sin_precipitacion()
        dict = {
            "prom_anual": promedio,
            "secHum": secHum,
            "mes": mensuales,
            "anios": anuales,
            "percentiles_diarios": percentiles_diarios,
            "percentiles_horarios": percentiles_horarios,
            "max_hora": max_hora,
            "dias_sin_precipitacion": dias_sin_precipitacion,
        }
        # print(dict)

        return dict


# """Esta clase se encarga de calcular los indicadores de precipitación,
# Cada funcion de la clase calcula un indicador determinado"""
#
# class IndicadoresPrecipitacion_orig():
#     def __init__(self, estacion_id, inicio, fin, completo):
#         self.estacion = estacion_id
#         self.inicio = inicio
#         self.fin = fin + timedelta(hours=23, minutes=59, seconds=59)
#         self.completo = completo
#
#     def rr_anual(self):
#         print(self.inicio,self.fin)
#         """precipitacion media anual precipitacion promedio del rango de fechas seleccionada"""
#         rranual = anio.Var1Anual.objects.filter(estacion_id__exact = self.estacion,fecha__gte=self.inicio,
#                                                    fecha__lte = self.fin, valor__isnull=False).order_by('fecha')
#
#         if rranual is not None:
#             return rranual
#         else:
#             return None
#
#     def rr_mensual(self):
#         """ devuelve la tabla de datos mensuales para la fecha seleccionadas"""
#         rrmensual = mes.Var1Mensual.objects.filter(estacion_id__exact = self.estacion,fecha__gte=self.inicio,
#                                                     fecha__lte = self.fin).order_by('fecha')
#         if rrmensual is not None:
#             return rrmensual
#         else:
#             return None
#
#     def rr_max_hora(self):
#         """calcula la precipitacion maxima acumulada en 24 horas"""
#         datos = vali.Var1Validado.objects.filter(estacion_id__exact=self.estacion, fecha__gte=self.inicio,
#                                 fecha__lte=self.fin, valor__isnull=False).order_by('fecha').values('fecha', 'valor')
#         df = pd.DataFrame.from_records(datos)
#         df['valor'] = pd.to_numeric(df['valor'])
#         minutos_inicio = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]
#         maximos = []
#         fechas = []
#         for i in minutos_inicio:
#             df['offset'] = df['fecha'] - timedelta(minutes=i)
#             df2 = df[df['offset'] >= self.inicio]
#             df2['offset'] = df['offset'].dt.floor('h')
#             dfr = df2.groupby('offset').agg({'valor': 'sum'})
#             idx = dfr['valor'].idxmax()
#             val = dfr['valor'][idx]
#             maximos.append(val)
#             fechas.append(idx)
#         maximo = max(maximos)
#         max_idx = maximos.index(maximo)
#         offset = minutos_inicio[max_idx]
#         fecha_ini = fechas[max_idx] + timedelta(minutes=offset) - timedelta(minutes=5)
#         fecha_fin = fecha_ini + timedelta(hours=1)
#         return {
#             'valor_max':maximo,
#             'fecha_ini':fecha_ini.strftime("%Y/%m/%d %H:%M:%S"),
#             'fecha_fin': fecha_fin.strftime("%Y/%m/%d %H:%M:%S"),
#         }
#
#     def percentilesDiarios(self):
#         """Calcula los percentelies en base a los datos diarios"""
#         diarios = list(dia.Var1Diario.objects.filter(
#             estacion_id__exact=self.estacion,fecha__gte=self.inicio,
#             fecha__lte=self.fin, valor__isnull=False, valor__gt=0
#         ).values_list('valor'))
#         # print("typo de datos en percentiles ", type(diarios))
#         # print(diarios)
#         a = np.array(diarios, dtype=object)
#         q10 = round(np.percentile(a, 10,  interpolation='lower'), 1)
#         q95 = round(np.percentile(a, 95, interpolation='lower'), 1)
#         return {'q10': q10, 'q95': q95}
#
#     def percentilesHorarios(self):
#         """Calcula los percentelies en base a los horarios"""
#         horarios = list(hora.Var1Horario.objects.filter(
#             estacion_id__exact=self.estacion,fecha__gte=self.inicio,
#             fecha__lte=self.fin, valor__isnull=False, valor__gt=0
#         ).values_list('valor'))
#         a = np.array(horarios, dtype=object)
#         q10 = round(np.percentile(a, 10, interpolation='lower'), 1)
#         q95 = round(np.percentile(a, 95, interpolation='lower'), 1)
#         return {'q10': q10, 'q95': q95}
#
#     def calcular_dias_sin_precipitacion(self):
#         sql = """
#         SELECT COUNT(*) FROM diario_var1diario
#         WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s AND valor = 0.0;
#         """
#         with connection.cursor() as cursor:
#             cursor.execute(sql, [self.estacion, self.inicio, self.fin])
#             resultado = cursor.fetchall()
#         return resultado[0][0]
#
#     def makeDic(self):
#         anuales = self.rr_anual()
#         print(anuales)
#
#         anioSecoMin = 1000000
#         anioHumedoMax = 0
#         iter = 0
#         fechaMin = None
#         fechaMax = None
#         promedio = 0
#         print("años consultados ",anuales.count())
#         if anuales.count() == 0:
#             return None
#
#         for an in anuales:# controla que el año tenga mas de 11 meses
#             print("fecha anual =>  ",an.fecha, "valor", an.valor," completoHumbral ",an.completo_umbral)
#             #mescontado = mes.Precipitacion.objects.filter(estacion_id__exact = self.estacion,fecha__gte=self.inicio,
#             #                                        fecha__lte = self.fin, valor__isnull=False)
#
#             if an.completo_umbral > 50.0:
#                 promedio += an.valor
#                 if an.valor < anioSecoMin:
#                     anioSecoMin = an.valor;
#                     fechaMin = an.fecha
#                 if an.valor > anioHumedoMax:
#                     anioHumedoMax = an.valor
#                     fechaMax = an.fecha
#                 iter += 1
#             print("promedio ",promedio)
#
#         if promedio > 0:
#             promedio =  str(round((promedio/iter), 1))
#             secHum = {'anio_seco': str(round(anioSecoMin,1)), 'fechsec': fechaMin.strftime("%Y"), 'anio_humedo': str(round(anioHumedoMax,1)),
#                       'fechhum': fechaMax.strftime("%Y")}
#         else:
#             promedio="S/D"
#             secHum = {'anio_seco': 'S/D', 'fechsec': 'S/D', 'anio_humedo': 'S/D',
#                       'fechhum': 'S/D'}
#
#         max_hora= self.rr_max_hora()
#
#         mensuales = self.rr_mensual()
#         percentiles_horarios = self.percentilesHorarios()
#         percentiles_diarios = self.percentilesDiarios()
#
#         print("****************************dict *******************")
#         anual2json = serializers.serialize('json', anuales,fields=('fecha', 'valor',
#         'completo_mediciones', 'completo_umbral', 'dias_con_lluvia', 'dias_sin_lluvia', 'mes_lluvioso', 'mes_seco',
#         'mes_lluvioso_valor', 'mes_seco_valor', 'estacionalidad'))
#         anuales = json.loads(anual2json)
#         mes2json = serializers.serialize('json', mensuales,fields=('fecha','valor'))
#         mensuales= json.loads(mes2json)
#         dias_sin_precipitacion = self.calcular_dias_sin_precipitacion()
#         dict={'prom_anual': promedio, 'secHum': secHum, 'mes':mensuales, 'anios':anuales,
#               'percentiles_diarios':percentiles_diarios, 'percentiles_horarios':percentiles_horarios,
#               'max_hora':max_hora, 'dias_sin_precipitacion':dias_sin_precipitacion}
#         print(dict)
#
#         return dict


##### funcion de calculo de indicadores de caudal
def indicaCaudal(estacion_id, inicio, fin, completo):
    """Function to calculate flow indicators."""

    amax = None
    amin = None
    datos = 0
    if completo:
        fechas = mes.Var10Mensual.objects.filter(
            estacion_id__exact=estacion_id
        ).aggregate(Max("fecha"), Min("fecha"))
        amax = fechas["fecha__max"].year
        amin = fechas["fecha__min"].year
        datos = mes.Var10Mensual.objects.filter(estacion_id__exact=estacion_id)[:10]
    elif inicio is not None and fin is not None:
        amax = fin.year
        amin = inicio.year
        datos = mes.Var10Mensual.objects.filter(estacion_id__exact=estacion_id)[:10]

    print("buscara para los años", amax, amin)
    if amax is not None and amin and len(datos) > 2:
        iniconsu = datetime(amin, 1, 1, 0, 0, 0)
        finconsu = datetime(amax, 12, 31, 23, 59, 0)
        tcau = dia.Var10Diario.objects.filter(
            estacion_id__exact=estacion_id, fecha__gte=iniconsu, fecha__lte=finconsu
        ).aggregate(Avg("valor"), Min("valor"), Max("valor"))

        print("datos encontrados", tcau["valor__avg"])
        print(tcau)
        if tcau["valor__avg"] is None:
            return None
        camax = tcau["valor__max"]
        caavg = tcau["valor__avg"]
        camim = tcau["valor__min"]
        fdmax = dia.Var10Diario.objects.filter(
            estacion_id__exact=estacion_id,
            fecha__gte=iniconsu,
            fecha__lte=finconsu,
            valor__exact=tcau["valor__max"],
        ).values("fecha")[:1]
        fdmin = dia.Var10Diario.objects.filter(
            estacion_id__exact=estacion_id,
            fecha__gte=iniconsu,
            fecha__lte=finconsu,
            valor__exact=tcau["valor__min"],
        ).values("fecha")[:1]
        print("*****************************************")
        print(fdmax, fdmin)

        ### calculo de percentiles
        """Calcula los percentelies en base a los datos diarios"""

        tcau = list(
            dia.Var10Diario.objects.filter(
                estacion_id__exact=estacion_id,
                fecha__gte=iniconsu,
                fecha__lte=finconsu,
                valor__isnull=False,
            )
            .order_by("valor")
            .values_list("valor")
        )
        print("tipo de datos :", type(tcau))
        print(len(tcau))

        a = np.array(tcau, dtype=object)
        p10 = np.percentile(a, 5, interpolation="lower")
        p50 = np.percentile(a, 50, interpolation="lower")
        p95 = np.percentile(a, 95, interpolation="lower")

        cames = mes.Var10Mensual.objects.filter(
            estacion_id__exact=estacion_id, fecha__gte=iniconsu, fecha__lte=finconsu
        ).aggregate(Avg("valor"), Min("valor"), Max("valor"))
        caSeco = cames["valor__min"]
        fecmessec = mes.Var10Mensual.objects.filter(
            estacion_id__exact=estacion_id,
            fecha__gte=iniconsu,
            fecha__lte=finconsu,
            valor__exact=cames["valor__min"],
        )[:1]

        ####
        #### indicadores con lso caudales especificos
        ####

        est = Estacion.objects.get(est_id=estacion_id)
        inf = est.influencia_km
        print("influecia ", inf)
        dias_sin_caudal = calcular_dias_sin_caudal(estacion_id, inicio, fin)
        ###################
        años = list(range(inicio.year, fin.year + 1))
        tablac = pd.DataFrame(columns=list(range(1, 13)), index=años)

        res_caudal = (
            mes.Var10Mensual.objects.filter(
                estacion_id__exact=est.est_id, fecha__gte=inicio, fecha__lte=fin
            )
            .order_by("fecha")
            .values("id", "fecha", "valor")
        )
        res_caudal = pd.DataFrame.from_records(res_caudal)
        for e in list(range(0, len(res_caudal))):
            fecha = res_caudal.at[e, "fecha"]
            valor = res_caudal.at[e, "valor"]
            tablac.at[fecha.year, fecha.month] = valor
        tablac = tablac.rename(columns=dict_mes, inplace=False)
        tabla_caudal = tablac.to_html(index=True, na_rep="")

        ####################
        if inf is not None:
            print("Se calculara con caudales especificos con influencia ", inf)
            dic = {
                "cmax": str(round(camax, 3)),
                "fdmax": fdmax[0]["fecha"].strftime("%d/%m/%Y"),
                "cavg": str(round(caavg, 3)),
                "cmim": str(round(camim, 3)),
                "fdmin": fdmin[0]["fecha"].strftime("%d/%m/%Y"),
                "per10": str(round(p10, 3)),
                "per50": str(round(p50, 3)),
                "per95": str(round(p95, 3)),
                "inf": str(inf),
                "cmessec": str(round(caSeco, 3)),
                "fecmessec": fecmessec[0].fecha.strftime("%m/%Y"),
                "cmax_es": str(round(camax / inf, 3)),
                "fdmax_es": fdmax[0]["fecha"].strftime("%d/%m/%Y"),
                "cavg_es": str(round(caavg / inf, 3)),
                "cmim_es": str(round(camim / inf, 3)),
                "fdmin_es": fdmin[0]["fecha"].strftime("%d/%m/%Y"),
                "per10_es": str(round(p10 / inf, 3)),
                "per50_es": str(round(p50 / inf, 3)),
                "per95_es": str(round(p95 / inf, 3)),
                "cmessec_es": str(round(caSeco / inf, 3)),
                "fecmessec_es": fecmessec[0].fecha.strftime("%m/%Y"),
                "dias_sin_caudal": dias_sin_caudal,
                "tabla_caudal": tabla_caudal,
            }
            print(caSeco, caSeco / inf)
        else:
            print(
                "fecha del me mas secos ::::: ",
                type(fecmessec[0].fecha),
                fecmessec[0].fecha,
            )
            dic = {
                "inf": "vacio",
                "cmax": str(round(camax, 3)),
                "fdmax": fdmax[0]["fecha"].strftime("%d/%m/%Y"),
                "cavg": str(round(caavg, 3)),
                "cmim": str(round(camim, 3)),
                "fdmin": fdmin[0]["fecha"].strftime("%d/%m/%Y"),
                "per10": str(round(p10, 2)),
                "per50": str(round(p50, 3)),
                "per95": str(round(p95, 3)),
                "cmessec": str(round(caSeco, 3)),
                "fecmessec": fecmessec[0].fecha.strftime("%m/%Y"),
                "dias_sin_caudal": dias_sin_caudal,
                "tabla_caudal": tabla_caudal,
            }

        print("retorna el dicionario")
        return dic
    else:
        return None


def calcular_escorrentia(sitiocuenca, est_caudal, est_precipitacion, inicio, fin):
    años = list(range(inicio.year, fin.year + 1))
    tabla = pd.DataFrame(columns=list(range(1, 13)), index=años)

    res = (
        mes.Var10Mensual.objects.filter(
            estacion_id__exact=est_caudal.est_id, fecha__gte=inicio, fecha__lte=fin
        )
        .order_by("fecha")
        .values("id", "fecha", "valor")
    )
    res = pd.DataFrame.from_records(res)
    tablac = tabla.copy()
    for e in list(range(0, len(res))):
        fecha = res.at[e, "fecha"]
        valor = res.at[e, "valor"]
        tablac.at[fecha.year, fecha.month] = valor
    caudal_promedio_meses = tablac.mean(axis=0)
    caudal_promedio_serie = caudal_promedio_meses.mean()
    area_influencia = est_caudal.influencia_km
    caudal_mm = (
        Decimal(caudal_promedio_serie) * 24 * 3600 * 365 / (area_influencia * 1000000)
    )
    tablac = tablac.rename(columns=dict_mes, inplace=False)
    data_caudal = {
        "nombre_estacion": est_caudal.est_codigo,
        "tabla_html": tablac.to_html(index=True, na_rep=""),
    }

    precipitaciones = []
    data_precipitacion = []
    for ep in est_precipitacion:
        res = (
            mes.Var1Mensual.objects.filter(
                estacion_id__exact=ep.est_id, fecha__gte=inicio, fecha__lte=fin
            )
            .order_by("fecha")
            .values("id", "fecha", "valor")
        )
        res = pd.DataFrame.from_records(res)
        tablap = tabla.copy()
        for e in list(range(0, len(res))):
            fecha = res.at[e, "fecha"]
            valor = res.at[e, "valor"]
            tablap.at[fecha.year, fecha.month] = valor
        precip_promedio_meses = tablap.mean(axis=0)
        precip_acum_serie = precip_promedio_meses.sum()
        precipitaciones.append(precip_acum_serie)
        tablap = tablap.rename(columns=dict_mes, inplace=False)
        data_precipitacion.append(
            {
                "nombre_estacion": ep.est_codigo,
                "tabla_html": tablap.to_html(index=True, na_rep=""),
            }
        )
    precip_anual_promedio = np.array(precipitaciones).mean()

    escorrentia = caudal_mm / Decimal(precip_anual_promedio)
    escorrentia = escorrentia * 100
    res = {
        "escorrentia": round(escorrentia, 2),
        "area": round(area_influencia, 2),
        "caudal": data_caudal,
        "precipitacion": data_precipitacion,
    }
    return res


def calcular_dias_sin_caudal(estacion_id, inicio, fin):
    """Calculate days without flow."""

    sql = """
    SELECT COUNT(*) FROM diario_var10diario 
    WHERE estacion_id = %s AND fecha >= %s AND fecha <= %s AND valor = 0.0;
    """
    with connection.cursor() as cursor:
        cursor.execute(sql, [estacion_id, inicio, fin])
        resultado = cursor.fetchall()
    return resultado[0][0]
