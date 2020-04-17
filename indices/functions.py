from anuarios import anuario
from variable.models import Variable
import validacion.models as vali
import horario.models as hora
import diario.models as dia
import mensual.models as mes
import anual.models as anio
from anuarios.models import Precipitacion, Caudal
from datetime import datetime, timedelta
from django.db.models import Sum, Max, Min, Avg, Count
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
        tabla = var.var_modelo
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
            return vali.Precipitacion.objects.raw(sql)
        elif frecuencia == 1:  # 'Horario':
            print("entra en horarios")
            return hora.Precipitacion.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                                     fecha__lte=fin).values("id", "fecha", "valor")
        elif frecuencia == 2:  # 'Diario':
            return dia.Precipitacion.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                                    fecha__lte=fin).values("id", "fecha", "valor")
        else:  # 'Mensual':
            print("entra en mensuales")
            return mes.Precipitacion.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                                    fecha__lte=fin).values("id", "fecha", "valor")
    else:
        return None


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
            dic = {'fecha': d1[0]['fecha'].strftime("%m/%d/%Y %H:%M:%S"), 'valore1': str(d1[0]['valor']),
                   'acume1': str(acume1),
                   "valore2": str(d1[1]['valor']), "acume2": str(acume2)}
        data.append(dic)

    return data


def consultaPeriodos(estacion_id, frecuencia):
    fmax = None
    fmin = None
    estacion = None

    if frecuencia == 0:
        fmax = vali.Precipitacion.objects.filter(estacion_id__exact=estacion_id).order_by('fecha').values('fecha')[:1]
        fmin = vali.Precipitacion.objects.filter(estacion_id__exact=estacion_id).order_by('-fecha').values('fecha')[:1]
    elif frecuencia == 1:  # 'Horario':
        fmax = hora.Precipitacion.objects.filter(estacion_id__exact=estacion_id).order_by('fecha').values('fecha')[:1]
        fmin = hora.Precipitacion.objects.filter(estacion_id__exact=estacion_id).order_by('-fecha').values('fecha')[:1]
    elif frecuencia == 2:  # 'Diario':
        fmax = dia.Precipitacion.objects.filter(estacion_id__exact=estacion_id).order_by('fecha').values('fecha')[:1]
        fmin = dia.Precipitacion.objects.filter(estacion_id__exact=estacion_id).order_by('-fecha').values('fecha')[:1]
    else:  # 'Mensual':
        fmax = mes.Precipitacion.objects.filter(estacion_id__exact=estacion_id).order_by('fecha').values('fecha')[:1]
        fmin = mes.Precipitacion.objects.filter(estacion_id__exact=estacion_id).order_by('-fecha').values('fecha')[:1]
    estacion = Estacion.objects.filter(est_id__exact=estacion_id).values('est_codigo', 'est_nombre')[:1]

    return fmax, fmin, estacion


def intensidadDiracion(estacion_id, fechaini, fechafin):
    # horas de acumulacion (2,5,10,20,24,48)
    acu2h = acumulaHoras(estacion_id, fechaini, fechafin, 2)
    acu5h = acumulaHoras(estacion_id, fechaini, fechafin, 5)
    acu10h = acumulaHoras(estacion_id, fechaini, fechafin, 10)
    acu20h = acumulaHoras(estacion_id, fechaini, fechafin, 20)
    acu24h = acumulaHoras(estacion_id, fechaini, fechafin, 24)
    acu48h = acumulaHoras(estacion_id, fechaini, fechafin, 48)
    max1h = hora.Precipitacion.objects.filter(estacion_id__exact=estacion_id, fecha__gte=fechaini,
                                              fecha__lte=fechafin).aggregate(Max("valor"))
    if max1h['valor__max'] is not None:
        max1h = max1h['valor__max']
    else:
        max1h = 0
    if len(acu2h) > 0:
        max2h = max(acu2h)
    else:
        max2h = 0
    if len(acu5h) > 0:
        max5h = max(acu5h)
    else:
        max5h = 0
    if len(acu10h) > 0:
        max10h = max(acu10h)
    else:
        max10h = 0
    if len(acu20h) > 0:
        max20h = max(acu20h)
    else:
        max20h = 0
    if len(acu24h) > 0:
        max24h = max(acu24h)
    else:
        max24h = 0
    if len(acu48h) > 0:
        max48h = max(acu48h)
    else:
        max48h = 0
    datadict = {}
    datadict.update(
         [("h1", str(max1h)), ("h2", str(max2h)), ("h5", str(max5h)), ("h10", str(max10h)), ("h20", str(max20h)),
          ("h24", str(max24h)), ("h48", str(max48h))])
    # datadict.update(
    #     [("h1", str(max48h)), ("h2", str(max24h)), ("h5", str(max20h)), ("h10", str(max10h)), ("h20", str(max5h)),
    #      ("h24", str(max2h)), ("h48", str(max1h))])
    print(datadict)
    return datadict


def acumulaHoras(estacion_id, fechaini, fechafin, nhoras):
    """acumula cada n horas u devuelve la serie dedatos """
    acumulados = []
    print("acumulando cada ", nhoras, " horas")
    # fechafin = fechaini
    # print(fechaini, " -- ", fechafin)
    while (fechaini <= fechafin):
        fechatemp = fechaini + timedelta(hours=nhoras)
        datohora = hora.Precipitacion.objects.filter(estacion_id__exact=estacion_id,
                                                     fecha__gte=fechaini, fecha__lt=fechatemp).aggregate(Sum("valor"))
        #print(datohora['valor__sum'])
        if datohora['valor__sum'] is not None:
            acumulados.append(datohora['valor__sum'])
            # print(fechaini, " -- ", fechatemp," : ",datohora['valor__sum'])
        fechaini = fechatemp
    return acumulados
def acumula5min():
    # aqui csultar los datos istantaneos
    valid = vali.Precipitacion.objects.all()[:10]
    #-na fucioque se desplace solo cadas5 minutos
    return "Hola mundo"

def acumulaSimple(est1, frecuencia):
    # print("metodo acumular")
    data = []
    acume1 = 0
    acumTme1 = 0
    # print("entra en el else")
    # print("Imprimiendo datos ")
    for d1 in est1:
        # print(d1[0]['valor'])
        if frecuencia == 0:
            acumTme1 = d1[0].valor
            acume1 = acume1 + acumTme1
            dic = {'fecha': d1[0].fecha.strftime("%m/%d/%Y %H:%M:%S"), 'valore1': str(d1[0].valor),
                   'acume1': str(acume1), "valore2": str(d1[1].valor), "acume2": str(acume2)}
            # dic = {'fecha': d1[0].fecha.strftime("%m/%d/%Y %H:%M:%S"), 'valore1': d1[0].valor,
            #        'acume1': acume1, "valore2": d1[1].valor, "acume2": acume2}
        else:
            acumTme1 = d1[0]['valor']
            acume1 = acume1 + acumTme1
            acumTme2 = d1[1]['valor']
            acume2 = acume2 + acumTme2
            dic = {'fecha': d1[0]['fecha'].strftime("%m/%d/%Y %H:%M:%S"), 'valore1': str(d1[0]['valor']),
                   'acume1': str(acume1),
                   "valore2": str(d1[1]['valor']), "acume2": str(acume2)}
        data.append(dic)
    print(data)
    return data

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
            df['CauEsp'] = round(df['CauEsp'].astype(float),6)
            df = df.sort_values(by=['valor'], ascending=[True])
            td = len(df['valor'])
            df['valor'] = round(df['valor'].astype(float),2)
            df['rango'] = range(1, td + 1)
            df['frecuencia'] = round((df['rango'] / td) * 1,9)
            df['valor'] = df['valor'].values[::-1]
            df['CauEsp'] = df['CauEsp'].values[::-1]
            listanual['cau'+str(anio)] = df['valor'].fillna('null').tolist()
            listanual['cauEsp'+str(anio)] = df['CauEsp'].fillna('null').tolist()
            listanual['fre'+str(anio)] = df['frecuencia'].fillna('null').tolist()
    if len(totaldf) > 30:
        totaldf['CauEsp'] = totaldf['valor'] / div
        totaldf['CauEsp'] = round(totaldf['CauEsp'].astype(float), 6)
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
    return json.dumps(dian, allow_nan=True,cls=DecimalEncoder)


def getCaudalanio(frecuencia, estacion_id,anio):
    #print("frecuencia", "estacion_id","anio")
    #print('   ',frecuencia,"   ", estacion_id,"   ","    ",anio)
    fi=str(anio)+"-01-01"
    ff = str(anio)+ "-12-31"
    inicio = datetime.strptime(fi,'%Y-%m-%d')
    fin = datetime.strptime(ff,'%Y-%m-%d')
    if frecuencia == 1:  # 'Horario':
        #print("entra en horario frecuencia ", frecuencia, estacion_id, inicio)
        hq = hora.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                             fecha__lte=fin, valor__isnull=False).values("valor")
        #print(hq.query)
        return hq
    if frecuencia == 2:  # 'Diario':
        #print("entra en diario ",frecuencia)
        dq = dia.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                           fecha__lte=fin, valor__isnull=False).values("valor")
        #print(dq.query)
        return dq
    return None

def getCaudalFrecMulti(listEst,fin,ffi):
    print("getCaudalFrecMulti:")
    if len(listEst) > 0 :
        listanual = {}
        for est in listEst:
            print(est)
            esta = Estacion.objects.get(est_id=est.est_id)
            inf = esta.influencia_km
            if inf is None:
                div = 1
            elif inf > 0:
                div = inf
            else:
                div = 1
            dq = dia.Caudal.objects.filter(estacion_id__exact=est, fecha__gte=fin,
                                           fecha__lte=ffi, valor__isnull=False).values("valor")
            if dq is not None and len(dq) > 30:
                df = pd.DataFrame(dq)
                totaldf = pd.concat([totaldf, df])
                df['CauEsp'] = df['valor'] / div
                df['CauEsp'] = round(df['CauEsp'].astype(float), 6)
                df = df.sort_values(by=['valor'], ascending=[True])
                td = len(df['valor'])
                df['valor'] = round(df['valor'].astype(float), 2)
                df['rango'] = range(1, td + 1)
                df['frecuencia'] = round((df['rango'] / td) * 1, 9)
                df['valor'] = df['valor'].values[::-1]
                df['CauEsp'] = df['CauEsp'].values[::-1]
                listanual['cau' + str(anio)] = df['valor'].fillna('null').tolist()
                listanual['cauEsp' + str(anio)] = df['CauEsp'].fillna('null').tolist()
                listanual['fre' + str(anio)] = df['frecuencia'].fillna('null').tolist()
        return json.dumps(listanual, allow_nan=True,cls=DecimalEncoder)
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
        rranual = anio.Precipitacion.objects.filter(estacion_id__exact = self.estacion,fecha__gte=self.inicio,
                                                   fecha__lte = self.fin, valor__isnull=False).order_by('fecha')

        if rranual is not None:
            return rranual
        else:
            return None

    def rr_mensual(self):
        """ devuelve la tabla de datos mensuales para la fecha seleccionadas"""
        rrmensual = mes.Precipitacion.objects.filter(estacion_id__exact = self.estacion,fecha__gte=self.inicio,
                                                    fecha__lte = self.fin).order_by('fecha')
        if rrmensual is not None:
            return rrmensual
        else:
            return None
    def rr_max_hora(self):
        """calcula la precipitacion maxima acumulada en 24 horas"""
        rr_hora = hora.Precipitacion.objects.filter(estacion_id__exact=self.estacion, fecha__gte=self.inicio,
                                          fecha__lte=self.fin, valor__isnull=False).aggregate(Max('valor'))
        fhormax = hora.Precipitacion.objects.filter(estacion_id__exact=self.estacion, fecha__gte=self.inicio,
                                                    fecha__lte=self.fin, valor__exact=rr_hora["valor__max"]).values(
            'fecha')[:1]
        #print("maxima precipit")
        #print(rr_hora['valor__max'])
        #print(fhormax[0]['fecha'].strftime("%d/%m/%Y %H:%M:%S" ))
        return {'valor_max':rr_hora['valor__max'],'fecha':fhormax[0]['fecha'].strftime("%d/%m/%Y %H:%M:%S" )}


    def percentilesDiarios(self):
        """Calcula los percentelies en base a los datos diarios"""
        diarios = list(dia.Precipitacion.objects.filter(estacion_id__exact = self.estacion,fecha__gte=self.inicio,
                                                    fecha__lte = self.fin, valor__isnull=False).values_list('valor'))
        # print("typo de datos en percentiles ", type(diarios))
        # print(diarios)
        a = np.array(diarios, dtype=object)
        q10 = np.percentile(a,10,  interpolation='lower')
        q95 = np.percentile(a, 95, interpolation='lower')
        return {'q10':q10,'q95':q95}

    def makeDic(self):
        anuales = self.rr_anual()
        print(anuales)

        anioSecoMin = 1000000
        anioHumedoMax = 0
        iter = 0
        fechaMin = None
        fechaMax = None
        promedio = -1
        print("años consultados ",anuales.count())
        if anuales.count() is 0:
            return None

        for an in anuales:# controla que el año tenga mas de 11 meses
            print("fecha anual =>  ",an.fecha)
            #mescontado = mes.Precipitacion.objects.filter(estacion_id__exact = self.estacion,fecha__gte=self.inicio,
            #                                        fecha__lte = self.fin, valor__isnull=False)
            if an.completo_umbral > 89.0:
                promedio += an.valor
                if an.valor < anioSecoMin:
                    anioSecoMin = an.valor;
                    fechaMin = an.fecha
                if an.valor > anioHumedoMax:
                    anioHumedoMax = an.valor
                    fechaMax = an.fecha
                iter += 1
        if promedio is not None:
            promedio =  str(round(promedio/iter,2))
            secHum = {'anio_seco': str(anioSecoMin), 'fechsec': fechaMin.strftime("%Y"), 'anio_humedo': str(anioHumedoMax),
                      'fechhum': fechaMax.strftime("%Y")}
        else:
            promedio="S/D"
            secHum = {'anio_seco': 'S/D', 'fechsec': 'S/D', 'anio_humedo': 'S/D',
                      'fechhum': 'S/D'}

        max24=self.rr_max_hora()
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
        dict={'prom_anual':promedio,'secHum': secHum,'mes':mensuales , 'anios':anuales, 'percen':per,'max24':max24}
        print(dict)

        return dict

##### funcion de calculo de indicadores de caudal
def indicaCaudal(estacion_id, inicio, fin, completo):
    amax = None
    amin = None
    datos = 0
    if completo:
        fechas = mes.Caudal.objects.filter(estacion_id__exact=estacion_id).aggregate(Max('fecha'), Min('fecha'))
        amax = fechas['fecha__max'].year
        amin = fechas['fecha__min'].year
        datos = mes.Caudal.objects.filter(estacion_id__exact=estacion_id)[:10]
    elif inicio is not None and fin is not None:
        amax = fin.year
        amin = inicio.year
        datos = mes.Caudal.objects.filter(estacion_id__exact=estacion_id)[:10]

    print("buscara para los años", amax,amin)
    if amax is not None and amin and len(datos) > 2:
        iniconsu = datetime(amin, 1, 1, 0, 0, 0)
        finconsu = datetime(amax, 12, 31, 23, 59, 0)
        tcau = dia.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu,
                                         fecha__lte=finconsu).aggregate(Avg('valor'), Min('valor'), Max('valor'))

        print("datos encontrados",tcau['valor__avg'])
        print(tcau)
        if tcau['valor__avg'] is None:
            return None
        camax = tcau["valor__max"]
        caavg = tcau["valor__avg"]
        camim = tcau["valor__min"]
        fdmax = dia.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu, fecha__lte=finconsu,
                                          valor__exact=tcau["valor__max"]).values('fecha')[:1]
        fdmin = dia.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu, fecha__lte=finconsu,
                                          valor__exact=tcau["valor__min"]).values('fecha')[:1]
        print("*****************************************")
        print(fdmax, fdmin)


        ### calculo de percentiles
        """Calcula los percentelies en base a los datos diarios"""

        tcau = list(dia.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu,
                                         fecha__lte=finconsu, valor__isnull=False).order_by("valor").values_list('valor'))
        print("tipo de datos :",type(tcau))
        print(len(tcau))

        a = np.array(tcau, dtype=object)
        p10 = np.percentile(a, 5, interpolation='lower')
        p50 = np.percentile(a, 50, interpolation='lower')
        p95 = np.percentile(a, 95, interpolation='lower')

        cames = mes.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu,
                                          fecha__lte=finconsu).aggregate(Avg('valor'), Min('valor'), Max('valor'))
        caSeco = cames["valor__min"]
        fecmessec = mes.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu,
                                          fecha__lte=finconsu, valor__exact=cames["valor__min"])[:1]

        ####
        #### indicadores con lso caudales especificos
        ####

        est = Estacion.objects.get(est_id=estacion_id)
        inf = est.influencia_km
        if inf is not None:
            print("Se calculara con caudales especificos con influencia ", inf)
            dic = {"cmax": str(round(camax, 7)), "fdmax": fdmax[0]['fecha'].strftime("%d/%m/%Y"),
                   "cavg": str(round(caavg, 7)), "cmim": str(round(camim, 7)),
                   "fdmin": fdmin[0]['fecha'].strftime("%d/%m/%Y"), "per10": str(round(p10, 7)),
                   "per50": str(round(p50, 7)), "per95": str(round(p95, 7)),
                   "inf":str(inf),"cmessec": str(round(caSeco, 7)),"fecmessec":fecmessec[0].fecha.strftime("%m/%Y"),
                   "cmax_es": str(round(camax/inf, 7)), "fdmax_es": fdmax[0]['fecha'].strftime("%d/%m/%Y"),
                   "cavg_es": str(round(caavg/inf, 7)), "cmim_es": str(round(camim/inf, 7)),
                   "fdmin_es": fdmin[0]['fecha'].strftime("%d/%m/%Y"), "per10_es": str(round(p10/inf, 2)),
                   "per50_es": str(round(p50/inf, 7)), "per95_es": str(round(p95/inf, 7)),
                  "cmessec_es": str(round(caSeco/inf, 7)), "fecmessec_es": fecmessec[0].fecha.strftime("%m/%Y")
                }
        else:
            print("fecha del me mas secos ::::: ",type(fecmessec[0].fecha),fecmessec[0].fecha)
            dic = {"inf":"vacio","cmax": str(round(camax, 7)), "fdmax": fdmax[0]['fecha'].strftime("%d/%m/%Y"),
                   "cavg": str(round(caavg, 7)), "cmim": str(round(camim, 7)),
                   "fdmin": fdmin[0]['fecha'].strftime("%d/%m/%Y"), "per10": str(round(p10, 2)),
                   "per50": str(round(p50, 7)), "per95": str(round(p95, 7)),
                   "cmessec": str(round(caSeco, 7)), "fecmessec":fecmessec[0].fecha.strftime("%m/%Y")
                   }
            print(caSeco, caSeco / inf)
        return dic
    else:
        return None


