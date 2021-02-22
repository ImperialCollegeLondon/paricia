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

#from anuarios import anuario
from variable.models import Variable
import validacion.models as vali
import horario.models as hora
import diario.models as dia
import mensual.models as mes
import anual.models as anio
# from anuarios.models import Var1Anuarios
from datetime import datetime, timedelta
from django.db.models import Sum, Max, Min, Avg, Count
from django.db import connection
from estacion.models import Estacion
import pandas as pd
import decimal
import numpy as np
from decimal import Decimal
import json

from django.core import serializers

class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            return {'__Decimal__': str(obj)}
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
        0: 'validado',
        1: 'diario',
        2: 'horario',
        3: 'mensual',
    }
    return switcher.get(i, "valor invalido")


# retorna la lista de datos validado, dado el id de variable, la estacion, fecha inicio y fecha fin
def getVarValidado(varid, estacion_id, inicio, fin, frecuencia):
    try:
        var = Variable.objects.get(var_id__exact=varid)
        tabla = var.var_codigo  #varcodigo
    except Variable.DoesNotExist:
        var = None

    print("frecuencia desde el view", frecuencia)
    # print(globals())
    if var is not None and estacion_id is not None:
        # print("desde el metodo validacion.functions.getVarValidado")
        if frecuencia == 0:
            print("Fecha inicio " + inicio.strftime("%m-%d-%Y %H:%M:%S") + " fecha fin " + fin.strftime(
                "%m-%d-%Y %H:%M:%S"))
            print("Estacion id " + str(estacion_id))
            sql = "WITH seleccion AS (" \
                  "SELECT id, fecha, valor, validacion FROM validacion_" + tabla.lower() + " WHERE estacion_id = " + str(
                estacion_id) + \
                  " and fecha >= '" + inicio.strftime("%d-%m-%Y %H:%M:%S") + "' and fecha <= '" + fin.strftime(
                "%d-%m-%Y %H:%M:%S") + "'" \
                                       ") SELECT ss.id, ss.fecha, ss.valor FROM (" \
                                       "SELECT fecha, MAX(validacion) AS validacion FROM seleccion GROUP BY fecha " \
                                       ") AS tbl_max " \
                                       "INNER JOIN seleccion ss ON ss.fecha = tbl_max.fecha " \
                                       "AND ss.validacion = tbl_max.validacion ORDER BY ss.fecha;"
            # print(sql)
            return vali.Var1Validado.objects.raw(sql)
        elif frecuencia == 1:  # 'Horario':
            print("entra en horarios")
            return hora.Var1Horario.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                                     fecha__lte=fin).values("id", "fecha", "valor")
        elif frecuencia == 2:  # 'Diario':
            return dia.Var1Diario.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                                    fecha__lte=fin).values("id", "fecha", "valor")
        else:  # 'Mensual':
            print("entra en mensuales")
            return mes.Var1Mensual.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                                    fecha__lte=fin).values("id", "fecha", "valor")
    else:
        return None

#Doblemasa
def acumularDoble(est1, est2, frecuencia):
    # print("metodo acumular")
    data = []
    ''' fechas = []
    valor = [] '''
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
            dic = {'fecha': d1[0].fecha.strftime("%m/%d/%Y %H:%M:%S"), 'valore1': str(d1[0].valor),
                   'acume1': str(acume1), "valore2": str(d1[1].valor), "acume2": str(acume2)}
            # dic = {'fecha': d1[0].fecha.strftime("%m/%d/%Y %H:%M:%S"), 'valore1': d1[0].valor,
            #        'acume1': acume1, "valore2": d1[1].valor, "acume2": acume2}
        else:
            acumTme1 = d1[0]['valor']
            acume1 = acume1 + acumTme1
            acumTme2 = d1[1]['valor']
            acume2 = acume2 + acumTme2
            dic = {'fecha': d1[0]['fecha'].strftime("%Y%m/%d/%Y %H:%M:%S"), 'valore1': str(d1[0]['valor']),
                   'acume1': str(acume1),
                   "valore2": str(d1[1]['valor']), "acume2": str(acume2)}
        data.append(dic)

    return data

#doblemasa
def consultaPeriodos(estacion_id, frecuencia):
    fmax = None
    fmin = None
    estacion = None

    if frecuencia == 0:
        fmax = vali.Var1Validado.objects.filter(estacion_id__exact=estacion_id).order_by('fecha').values('fecha')[:1]
        fmin = vali.Var1Validado.objects.filter(estacion_id__exact=estacion_id).order_by('-fecha').values('fecha')[:1]
    elif frecuencia == 1:  # 'Horario':
        fmax = hora.Var1Horario.objects.filter(estacion_id__exact=estacion_id).order_by('fecha').values('fecha')[:1]
        fmin = hora.Var1Horario.objects.filter(estacion_id__exact=estacion_id).order_by('-fecha').values('fecha')[:1]
    elif frecuencia == 2:  # 'Diario':
        fmax = dia.Var1Diario.objects.filter(estacion_id__exact=estacion_id).order_by('fecha').values('fecha')[:1]
        fmin = dia.Var1Diario.objects.filter(estacion_id__exact=estacion_id).order_by('-fecha').values('fecha')[:1]
    else:  # 'Mensual':
        fmax = mes.Var1Mensual.objects.filter(estacion_id__exact=estacion_id).order_by('fecha').values('fecha')[:1]
        fmin = mes.Var1Mensual.objects.filter(estacion_id__exact=estacion_id).order_by('-fecha').values('fecha')[:1]
    estacion = Estacion.objects.filter(est_id__exact=estacion_id).values('est_codigo', 'est_nombre')[:1]

    return fmax, fmin, estacion

from time import time
def intensidadDiracion(estacion_id, fechaini, fechafin):
    tiempo_inicial = time()
    periodos = [5,10,15,30,60,120,1440]
    print(estacion_id, fechaini, fechafin)
    est = Estacion.objects.get(pk = estacion_id)
    c = connection.cursor()
    fechas =[]
    valores = []
    intensidad = []
    intervalos = []
    try:
        for p in periodos:
            c.execute("BEGIN")
            c.callproc('acumular',(estacion_id, fechaini, fechafin, p))
            result = c.fetchall()
            #print("result ",result)
            cad = result[0][0].split(";")
            maximo=float(cad[1])
            if maximo >= 0:
                fechas.append(cad[0])
                valores.append(maximo)
                intensidad.append(round(maximo/(p/60),1))
                intervalos.append(p)
        c.close()
    finally:
        c.close()
    if len(fechas) == 0:
        mensaje="No hay datos para procesar en la estacion "+str(est.est_codigo)+" en el año selecionado"
    else:
        mensaje="los cálculos se realizaron con éxito"

    tiempo_final = time()
    tiempo_ejecucion = tiempo_final - tiempo_inicial
    print("ejecutado en ",tiempo_ejecucion)
    datadict = {"estacion_id":est.est_codigo,"fecha":fechas,"maximo":valores,"inte":intensidad,'iterval':intervalos,'mensaje':mensaje}
    #print(datadict)
    return datadict


#### calcula los datos para la curva de duracion sin la influencia de la estacion
def getCaudalFrec(estacion_id, inicio, fin, frecuencia):
    """Calcula el caudal especifico de una estacion hidrológica"""
    est = Estacion.objects.get(est_id=estacion_id)
    inf = est.influencia_km
    print(estacion_id ,"influencia ", inf, "fecha ini :", inicio.year, type(inicio), " fecha fin: ", fin.year)
    anios=[]
    totaldf = pd.DataFrame()
    ainf = False;
    long = 0;
    if inf is None:
        div = 1
    elif inf > 0:
        div = inf
        ainf = True
    else:
        div = 1
    listanual = {}
    for anio in range(inicio.year,fin.year+1):
        print( "procesar año ",anio ,"valor del div", div, "ainf ",ainf)
        caudal = getCaudalanio(frecuencia,estacion_id,anio)
        if caudal is not None and len(caudal) > 30:
            anios.append(anio)
            if len(caudal) > long:
                long = len(caudal)
            df = pd.DataFrame(caudal)
            totaldf = pd.concat([totaldf, df])
            df['CauEsp'] = df['valor'] / div
            df['CauEsp'] = round(df['CauEsp'].astype(float),3)
            df = df.sort_values(by=['valor'], ascending=[True])
            td = len(df['valor'])
            df['valor'] = round(df['valor'].astype(float),3)
            df['rango'] = range(1, td + 1)
            df['frecuencia'] = round((df['rango'] / td) * 1,9)
            df['valor'] = df['valor'].values[::-1]
            df['CauEsp'] = df['CauEsp'].values[::-1]
            listanual['cau'+str(anio)] = df['valor'].fillna('null').tolist()
            listanual['cauEsp'+str(anio)] = df['CauEsp'].fillna('null').tolist()
            listanual['fre'+str(anio)] = df['frecuencia'].fillna('null').tolist()
    if len(totaldf) > 30:
        totaldf['CauEsp'] = totaldf['valor'] / div
        totaldf['CauEsp'] = round(totaldf['CauEsp'].astype(float), 3)
        totaldf = totaldf.sort_values(by=['valor'], ascending=[True])
        td = len(totaldf['valor'])
        totaldf['valor'] = round(totaldf['valor'].astype(float), 2)
        totaldf['rango'] = range(1, td + 1)
        totaldf['frecuencia'] = round((totaldf['rango'] / td) * 1, 9)
        totaldf['valor'] = totaldf['valor'].values[::-1]
        totaldf['CauEsp'] = totaldf['CauEsp'].values[::-1]
        totdic={'cau':totaldf['valor'].fillna('null').tolist(),'cauEsp':totaldf['CauEsp'].fillna('null').tolist(),
                'fre':totaldf['frecuencia'].fillna('null').tolist()}
        dian = { 'mayor':long,'aporte':ainf,'anios': anios, 'anuales':listanual, 'total':totdic}
    else:
        dian = None
    return dian
    #return json.dumps(dian, allow_nan=True,cls=DecimalEncoder)


def getCaudalanio(frecuencia, estacion_id,anio):
    #print("frecuencia", "estacion_id","anio")
    #print('   ',frecuencia,"   ", estacion_id,"   ","    ",anio)
    fi=str(anio)+"-01-01"
    ff = str(anio)+ "-12-31"
    inicio = datetime.strptime(fi,'%Y-%m-%d')
    fin = datetime.strptime(ff,'%Y-%m-%d')
    if frecuencia == 1:  # 'Horario':
        #print("entra en horario frecuencia ", frecuencia, estacion_id, inicio)
        hq = hora.Var10Horario.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                             fecha__lte=fin, valor__isnull=False).values("valor")#Cambiar aki
        #print(hq.query)
        return hq
    if frecuencia == 2:  # 'Diario':
        #print("entra en diario ",frecuencia)
        dq = dia.Var10Diario.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                           fecha__lte=fin, valor__isnull=False).values("valor")#Cambiar aki
        #print(dq.query)
        return dq
    return None

def getCaudalFrecMulti(listEst,fin,ffi):
    print("getCaudalFrecMulti:")
    if len(listEst) > 0:
        estaciones=[]
        calculos = {}
        codigos=[]
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
            dq = dia.Var10Diario.objects.filter(estacion_id__exact=est, fecha__gte=fin,
                                           fecha__lte=ffi, valor__isnull=False).values("valor",'fecha').order_by('fecha')

            if dq is not None and len(dq) > 30:
                df = pd.DataFrame(dq)
                #print(df.head(10))
                codigos.append(est)
                df['CauEsp'] = df['valor'] / div
                df['CauEsp'] = round(df['CauEsp'].astype(float), 3)
                df = df.sort_values(by=['valor'], ascending=[True])
                td = len(df['valor'])
                df['valor'] = round(df['valor'].astype(float), 2)
                df['rango'] = range(1, td + 1)
                df['frecuencia'] = round((df['rango'] / td) * 1, 9)
                df['valor'] = df['valor'].values[::-1]
                df['CauEsp'] = df['CauEsp'].values[::-1]
                calculos['cau' + str(est)] = df['valor'].fillna('null').tolist()
                calculos['cauEsp' + str(est)] = df['CauEsp'].fillna('null').tolist()
                calculos['fre' + str(est)] = df['frecuencia'].fillna('null').tolist()
                print("fecha inicio ",df['fecha'][0], "fecha fin ",df['fecha'][len(df)-1]  )
                estaciones.append({'estacion':esta.est_codigo,'inicio':df['fecha'][0].strftime("%d/%m/%Y") ,'fin':df['fecha'][len(df)-1].strftime("%d/%m/%Y")})
        #print(calculos)
        dict = {'estaciones':estaciones,'codigos':codigos,'datos':calculos}
        return json.dumps(dict, allow_nan=True,cls=DecimalEncoder)
    else:
        return None

"""Esta clase se encarga de calcular los indicadores de precipitación,
Cada funcion de la clase calcula un indicador determinado"""


class IndicadoresPrecipitacion():
    def __init__(self, estacion_id, inicio, fin, completo):
        self.estacion = estacion_id
        self.inicio = inicio
        self.fin = fin
        self.completo = completo

    def rr_anual(self):
        print(self.inicio,self.fin)
        """precipitacion media anual precipitacion promedio del rango de fechas seleccionada"""
        rranual = anio.Var1Anual.objects.filter(estacion_id__exact = self.estacion,fecha__gte=self.inicio,
                                                   fecha__lte = self.fin, valor__isnull=False).order_by('fecha')

        if rranual is not None:
            return rranual
        else:
            return None

    def rr_mensual(self):
        """ devuelve la tabla de datos mensuales para la fecha seleccionadas"""
        rrmensual = mes.Var1Mensual.objects.filter(estacion_id__exact = self.estacion,fecha__gte=self.inicio,
                                                    fecha__lte = self.fin).order_by('fecha')
        if rrmensual is not None:
            return rrmensual
        else:
            return None
    def rr_max_hora(self):
        """calcula la precipitacion maxima acumulada en 24 horas"""
        rr_hora = hora.Var1Horario.objects.filter(estacion_id__exact=self.estacion, fecha__gte=self.inicio,
                                          fecha__lte=self.fin, valor__isnull=False).aggregate(Max('valor'))
        fhormax = hora.Var1Horario.objects.filter(estacion_id__exact=self.estacion, fecha__gte=self.inicio,
                                                    fecha__lte=self.fin, valor__exact=rr_hora["valor__max"]).values(
            'fecha')[:1]
        #print("maxima precipit")
        #print(rr_hora['valor__max'])
        #print(fhormax[0]['fecha'].strftime("%d/%m/%Y %H:%M:%S" ))
        return {'valor_max':rr_hora['valor__max'],'fecha':fhormax[0]['fecha'].strftime("%d/%m/%Y %H:%M:%S" )}


    def percentilesDiarios(self):
        """Calcula los percentelies en base a los datos diarios"""
        diarios = list(dia.Var1Diario.objects.filter(estacion_id__exact = self.estacion,fecha__gte=self.inicio,
                                                    fecha__lte = self.fin, valor__isnull=False).values_list('valor'))
        # print("typo de datos en percentiles ", type(diarios))
        # print(diarios)
        a = np.array(diarios, dtype=object)
        q10 = round(np.percentile(a,10,  interpolation='lower'),1)
        q95 = round(np.percentile(a, 95, interpolation='lower'),1)
        return {'q10':q10,'q95':q95}

    def makeDic(self):
        anuales = self.rr_anual()
        print(anuales)

        anioSecoMin = 1000000
        anioHumedoMax = 0
        iter = 0
        fechaMin = None
        fechaMax = None
        promedio = 0
        print("años consultados ",anuales.count())
        if anuales.count() == 0:
            return None

        for an in anuales:# controla que el año tenga mas de 11 meses
            print("fecha anual =>  ",an.fecha, "valor", an.valor," completoHumbral ",an.completo_umbral)
            #mescontado = mes.Precipitacion.objects.filter(estacion_id__exact = self.estacion,fecha__gte=self.inicio,
            #                                        fecha__lte = self.fin, valor__isnull=False)

            if an.completo_umbral > 50.0:
                promedio += an.valor
                if an.valor < anioSecoMin:
                    anioSecoMin = an.valor;
                    fechaMin = an.fecha
                if an.valor > anioHumedoMax:
                    anioHumedoMax = an.valor
                    fechaMax = an.fecha
                iter += 1
            print("promedio ",promedio)

        if promedio > 0:
            promedio =  str(round((promedio/iter), 1))
            secHum = {'anio_seco': str(round(anioSecoMin,1)), 'fechsec': fechaMin.strftime("%Y"), 'anio_humedo': str(round(anioHumedoMax,1)),
                      'fechhum': fechaMax.strftime("%Y")}
        else:
            promedio="S/D"
            secHum = {'anio_seco': 'S/D', 'fechsec': 'S/D', 'anio_humedo': 'S/D',
                      'fechhum': 'S/D'}

        max24= self.rr_max_hora()
        #print("anio_seco :",anioSecoMin, "fechsec :", fechaMin.strftime("%m-%Y"),"anio_humedo :",anioHumedoMax, "fechhum:", fechaMax.strftime("%Y"))


        mensuales = self.rr_mensual()
        #print("*******************datos mensuales *******************")
        #print(mensuales)
        per = self.percentilesDiarios()

        print("****************************dict *******************")
        anual2json = serializers.serialize('json', anuales,fields=('fecha', 'valor',
        'completo_mediciones', 'completo_umbral', 'dias_con_lluvia', 'dias_sin_lluvia', 'mes_lluvioso', 'mes_seco',
        'mes_lluvioso_valor', 'mes_seco_valor', 'estacionalidad'))
        anuales = json.loads(anual2json)
        #print("type of anuales")
        #print(type(anuales))
        mes2json = serializers.serialize('json', mensuales,fields=('fecha','valor'))
        mensuales= json.loads(mes2json)
        dict={'prom_anual': promedio,'secHum': secHum,'mes':mensuales , 'anios':anuales, 'percen':per,'max24':max24}
        print(dict)

        return dict

##### funcion de calculo de indicadores de caudal
def indicaCaudal(estacion_id, inicio, fin, completo):
    amax = None
    amin = None
    datos = 0
    if completo:
        fechas = mes.Var10Mensual.objects.filter(estacion_id__exact=estacion_id).aggregate(Max('fecha'), Min('fecha'))
        amax = fechas['fecha__max'].year
        amin = fechas['fecha__min'].year
        datos = mes.Var10Mensual.objects.filter(estacion_id__exact=estacion_id)[:10]
    elif inicio is not None and fin is not None:
        amax = fin.year
        amin = inicio.year
        datos = mes.Var10Mensual.objects.filter(estacion_id__exact=estacion_id)[:10]

    print("buscara para los años", amax,amin)
    if amax is not None and amin and len(datos) > 2:
        iniconsu = datetime(amin, 1, 1, 0, 0, 0)
        finconsu = datetime(amax, 12, 31, 23, 59, 0)
        tcau = dia.Var10Diario.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu,
                                         fecha__lte=finconsu).aggregate(Avg('valor'), Min('valor'), Max('valor'))

        print("datos encontrados",tcau['valor__avg'])
        print(tcau)
        if tcau['valor__avg'] is None:
            return None
        camax = tcau["valor__max"]
        caavg = tcau["valor__avg"]
        camim = tcau["valor__min"]
        fdmax = dia.Var10Diario.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu, fecha__lte=finconsu,
                                          valor__exact=tcau["valor__max"]).values('fecha')[:1]
        fdmin = dia.Var10Diario.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu, fecha__lte=finconsu,
                                          valor__exact=tcau["valor__min"]).values('fecha')[:1]
        print("*****************************************")
        print(fdmax, fdmin)


        ### calculo de percentiles
        """Calcula los percentelies en base a los datos diarios"""

        tcau = list(dia.Var10Diario.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu,
                                         fecha__lte=finconsu, valor__isnull=False).order_by("valor").values_list('valor'))
        print("tipo de datos :",type(tcau))
        print(len(tcau))

        a = np.array(tcau, dtype=object)
        p10 = np.percentile(a, 5, interpolation='lower')
        p50 = np.percentile(a, 50, interpolation='lower')
        p95 = np.percentile(a, 95, interpolation='lower')

        cames = mes.Var10Mensual.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu,
                                          fecha__lte=finconsu).aggregate(Avg('valor'), Min('valor'), Max('valor'))
        caSeco = cames["valor__min"]
        fecmessec = mes.Var10Mensual.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu,
                                          fecha__lte=finconsu, valor__exact=cames["valor__min"])[:1]

        ####
        #### indicadores con lso caudales especificos
        ####

        est = Estacion.objects.get(est_id=estacion_id)
        inf = est.influencia_km
        print( "influecia ",inf)
        if inf is not None:
            print("Se calculara con caudales especificos con influencia ", inf)
            dic = {"cmax": str(round(camax, 3)), "fdmax": fdmax[0]['fecha'].strftime("%d/%m/%Y"),
                   "cavg": str(round(caavg, 3)), "cmim": str(round(camim, 3)),
                   "fdmin": fdmin[0]['fecha'].strftime("%d/%m/%Y"), "per10": str(round(p10, 3)),
                   "per50": str(round(p50, 3)), "per95": str(round(p95, 3)),
                   "inf":str(inf),"cmessec": str(round(caSeco, 3)),"fecmessec":fecmessec[0].fecha.strftime("%m/%Y"),
                   "cmax_es": str(round(camax/inf, 3)), "fdmax_es": fdmax[0]['fecha'].strftime("%d/%m/%Y"),
                   "cavg_es": str(round(caavg/inf, 3)), "cmim_es": str(round(camim/inf, 3)),
                   "fdmin_es": fdmin[0]['fecha'].strftime("%d/%m/%Y"), "per10_es": str(round(p10/inf, 3)),
                   "per50_es": str(round(p50/inf, 3)), "per95_es": str(round(p95/inf, 3)),
                  "cmessec_es": str(round(caSeco/inf, 3)), "fecmessec_es": fecmessec[0].fecha.strftime("%m/%Y")
                }
            print(caSeco, caSeco / inf)
        else:
            print("fecha del me mas secos ::::: ",type(fecmessec[0].fecha),fecmessec[0].fecha)
            dic = {"inf":"vacio","cmax": str(round(camax, 3)), "fdmax": fdmax[0]['fecha'].strftime("%d/%m/%Y"),
                   "cavg": str(round(caavg, 3)), "cmim": str(round(camim, 3)),
                   "fdmin": fdmin[0]['fecha'].strftime("%d/%m/%Y"), "per10": str(round(p10, 2)),
                   "per50": str(round(p50, 3)), "per95": str(round(p95, 3)),
                   "cmessec": str(round(caSeco, 3)), "fecmessec":fecmessec[0].fecha.strftime("%m/%Y")
                   }

        print("retorna el dicionario")
        return dic
    else:
        return None
