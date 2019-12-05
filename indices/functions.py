from variable.models import Variable
import validacion.models as vali
import horario.models as hora
import diario.models as dia
import mensual.models as mes
from anuarios.models import Precipitacion, Caudal
from datetime import datetime, timedelta
from django.db.models import Sum, Max, Min, Avg, Count
from estacion.models import Estacion
import pandas as pd
import decimal
import numpy as np

def periodos(i):
    switcher = {
        0: 'validado',
        1: 'diario',
        2: 'horario',
        3: 'mensual',
    }
    return switcher.get(i, "valor invalido")

#retorna la lista de datos validado, dado el id de variable, la estacion, fecha inicio y fecha fin
def getVarValidado(varid,estacion_id, inicio,fin,frecuencia):

    try:
        var = Variable.objects.get(var_id__exact=varid)
        tabla = var.var_modelo
    except Variable.DoesNotExist:
        var = None

    print("frecuencia desde el view",frecuencia)
    #print(globals())
    if var is not None and estacion_id is not None:
        # print("desde el metodo validacion.functions.getVarValidado")
        if frecuencia == 0:
            print("Fecha inicio "+inicio.strftime("%m-%d-%Y %H:%M:%S")+" fecha fin "+fin.strftime("%m-%d-%Y %H:%M:%S"))
            print("Estacion id "+str(estacion_id))
            sql = "WITH seleccion AS (" \
                  "SELECT id, fecha, valor, validacion FROM validacion_" + tabla.lower() + " WHERE estacion_id = " + str(estacion_id) + \
                  " and fecha >= '" + inicio.strftime("%d-%m-%Y %H:%M:%S") + "' and fecha <= '"+ fin.strftime("%d-%m-%Y %H:%M:%S") +"'" \
                   ") SELECT ss.id, ss.fecha, ss.valor FROM (" \
                   "SELECT fecha, MAX(validacion) AS validacion FROM seleccion GROUP BY fecha " \
                   ") AS tbl_max " \
                    "INNER JOIN seleccion ss ON ss.fecha = tbl_max.fecha " \
                    "AND ss.validacion = tbl_max.validacion ORDER BY ss.fecha;"
            #print(sql)
            return vali.Precipitacion.objects.raw(sql)
        elif frecuencia == 1: # 'Horario':
            print("entra en horarios")
            return hora.Precipitacion.objects.filter(estacion_id__exact=estacion_id,fecha__gte = inicio, fecha__lte = fin).values("id", "fecha", "valor")
        elif frecuencia == 2: #'Diario':
            return dia.Precipitacion.objects.filter(estacion_id__exact=estacion_id,fecha__gte = inicio, fecha__lte = fin).values("id", "fecha", "valor")
        else: #'Mensual':
            print("entra en mensuales")
            return mes.Precipitacion.objects.filter(estacion_id__exact=estacion_id,fecha__gte = inicio, fecha__lte = fin).values("id", "fecha", "valor")
    else:
        return None

def acumularDoble(est1, est2, frecuencia):
    #print("metodo acumular")
    data = []
    ''' fechas = []
    valor = [] '''
    acume1 = 0
    acume2 = 0
    acumTme1 = 0
    acumTme2 = 0
    #print("entra en el else")
    #print("Imprimiendo datos ")
    for d1 in zip(est1, est2):
        #print(d1[0]['valor'])
        if frecuencia == 0:
            acumTme1 = d1[0].valor
            acume1 = acume1 + acumTme1
            acumTme2 = d1[1].valor
            acume2 = acume2 + acumTme2
            dic = {'fecha':d1[0].fecha.strftime("%m/%d/%Y %H:%M:%S"),'valore1':str(d1[0].valor),'acume1':str(acume1),"valore2":str(d1[1].valor),"acume2":str(acume2)}
            # dic = {'fecha': d1[0].fecha.strftime("%m/%d/%Y %H:%M:%S"), 'valore1': d1[0].valor,
            #        'acume1': acume1, "valore2": d1[1].valor, "acume2": acume2}
        else:
            acumTme1 = d1[0]['valor']
            acume1 = acume1 + acumTme1
            acumTme2 = d1[1]['valor']
            acume2 = acume2 + acumTme2
            dic = {'fecha': d1[0]['fecha'].strftime("%m/%d/%Y %H:%M:%S"), 'valore1': str(d1[0]['valor']), 'acume1': str(acume1),
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
    estacion = Estacion.objects.filter(est_id__exact = estacion_id).values('est_codigo','est_nombre')[:1]

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
                                      fecha__lt=fechafin).aggregate(Max("valor"))
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
    datadict={}
    datadict.update([("h1",str(max1h)), ("h2",str(max2h)), ("h5",str(max5h)), ("h10",str(max10h)), ("h20",str(max20h)), ("h24",str(max24h)), ("h48",str(max48h))])
    return datadict

def acumulaHoras(estacion_id, fechaini, fechafin, nhoras):
    """acumula cada n horas u devuelve la serie dedatos """
    acumulados = []
    print("acumulando cada ",nhoras," horas")
    #fechafin = fechaini
    #print(fechaini, " -- ", fechafin)
    while (fechaini <= fechafin):
        fechatemp = fechaini + timedelta(hours=nhoras)
        datohora = hora.Precipitacion.objects.filter(estacion_id__exact=estacion_id,
                    fecha__gte=fechaini, fecha__lt=fechatemp).aggregate(Sum("valor"))
        if datohora['valor__sum'] is not None:
            acumulados.append(datohora['valor__sum'])
            #print(fechaini, " -- ", fechatemp," : ",datohora['valor__sum'])
        fechaini = fechatemp
    return acumulados

def acumulaSimple(est1,frecuencia):
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

def getCaudalFrec(estacion_id,inicio, fin,frecuencia):
    """Calcula el caudal especifico de una estacion hidrológica"""
    print("funcion caudal ")
    const = 0.0
    est = Estacion.objects.get(est_id=estacion_id)
    inf = est.influencia_km
    print("influencia ",inf, "fecha ini :",inicio," fecha fin: ",fin)
    #Qesp = Q / inf
    if frecuencia == 1:  # 'Horario':
        print("entra en horario frecuencia ",frecuencia)
        const = 1
        caudal = hora.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                                 fecha__lte=fin).values( "valor")
    elif frecuencia == 2:  # 'Diario':
        #print("entra en diario ",frecuencia)
        const = 1
        caudal =  dia.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                                fecha__lte=fin).values( "valor")
    else:  # 'Mensual':
        #print("entra en mensuales ,frecuencia")
        caudal = mes.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                                fecha__lte=fin).values('fecha','valor')


    if caudal is not None and len(caudal) > 0 and inf is not None:
        df = pd.DataFrame(caudal)
        df['CauEsp'] = df['valor']/inf * decimal.Decimal(const)
        df = df.sort_values(by=['CauEsp'], ascending=[True])
        td = len(df['CauEsp'])
        df['rango'] = range(1, td+1)
        df['frecuencia'] = (df['rango']/td) * 1
        return df.to_json(orient='records')
    else:
        return None

def caudalEspecifico(caudal, estacion_id, frecuencia):
    const = 0
    est = Estacion.objects.get(est_id=estacion_id)
    inf = est.influencia_km
    if frecuencia == 1:
        const = 0.0036
    elif frecuencia == 2:
        const = 0.0864
    if inf is not None:
        caudal

def IndicaPreci(estacion_id,inicio,fin,completo):

    amax = None
    amin = None
    datos = 0
    if completo:
        fechas = mes.Precipitacion.objects.filter(estacion_id__exact=estacion_id).aggregate(Max('fecha'), Min('fecha'))
        print(fechas)
        if fechas['fecha__max'] is not None and fechas['fecha__min'] is not None:
            amax = fechas['fecha__max'].year
            amin = fechas['fecha__min'].year
            datos = mes.Precipitacion.objects.filter(estacion_id__exact=estacion_id)[:10]
    elif inicio is not None and fin is not None:
        amax = fin.year
        amin = inicio.year
        datos = mes.Precipitacion.objects.filter(estacion_id__exact=estacion_id)[:10]
        print("Buscar segun las fechas")

    if amax is not None and amin and len(datos) > 2:
        #print("min",amin,"max",amax)
        iniconsu = datetime(amin,1,1,0,0,0)
        finconsu = datetime(amax,12,31,23,59,0)
        con = 0
        acum = 0
        maxAnual = -1
        minAnual = 99999
        fechaMaxAnual = None
        fechaMinAnual = None
        for i in range(amin, amax):
            #print("Buscar en ", str(i)+"-01-01",str(i+1)+"-01-01")
            tmes = mes.Precipitacion.objects.filter(estacion_id__exact=estacion_id, fecha__gte=str(i)+"-01-01", fecha__lt=str(i+1)+"-01-01").aggregate(Count('fecha'),Sum('valor'))
            #print(tmes)
            if(tmes["fecha__count"] == 12):
                #print("Perfecto estamos completos")
                #print("len",len(tmes),tmes, "con ", con)
                if tmes['valor__sum'] > maxAnual:
                    maxAnual = tmes["valor__sum"]
                    fechaMaxAnual = i
                if tmes['valor__sum'] < minAnual:
                    minAnual = tmes["valor__sum"]
                    fechaMinAnual = i
                acum = acum + tmes["valor__sum"]
                con = con + 1
        if con == 0:
            rranual= 0.0
        else:
            rranual = round(acum / con,2)
        tmes = mes.Precipitacion.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu, fecha__lte=finconsu).aggregate(Avg('valor'),Min('valor'),Max('valor'))
        fmeMax = mes.Precipitacion.objects.filter(estacion_id__exact=estacion_id,fecha__gte=iniconsu, fecha__lte=finconsu, valor__exact = tmes["valor__max"]).values('fecha')[:1]
        fmeMin = mes.Precipitacion.objects.filter(estacion_id__exact=estacion_id,fecha__gte=iniconsu, fecha__lte=finconsu, valor__exact = tmes["valor__min"]).values('fecha')[:1]
        #print(fmeMax[0]['fecha'])
        rrmes = round(tmes["valor__avg"],2)
        rrSeco = round(tmes["valor__min"],2)
        rrlluvia = round(tmes["valor__max"], 2)
        tdia = dia.Precipitacion.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu,
                                                fecha__lte=finconsu).values('valor')
        print(tdia)
        dccl = 0
        temdccl = 0
        dcsl = 0
        temdcsl = 0
        for i in tdia:
            print(i['valor'])
            if i['valor'] is not None:
                if i['valor'] == 0:
                    temdcsl = temdcsl + 1
                    if temdcsl > dcsl :
                        dcsl = temdcsl
                else:
                    temdcsl = 0
                if i['valor'] > 0.1:
                    temdccl = temdccl + 1
                    if temdccl > dccl:
                        dccl = temdccl
                else:
                    temdccl = 0


        tdia = dia.Precipitacion.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu,
                                                fecha__lte=finconsu).order_by("valor")
        total_count = tdia.count()
        p10 = posi(total_count, 10)
        p95 = posi(total_count, 95)
        print(total_count, p10, p95)
        cap10 = tdia[p10].valor
        cap95 = tdia[p95].valor
        print(tdia[p10-1].valor,tdia[p10].valor,tdia[p10+1].valor)
        thora = hora.Precipitacion.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu, fecha__lte=finconsu).aggregate(Avg('valor'), Min('valor'), Max('valor'))
        fhormax = hora.Precipitacion.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu, fecha__lte=finconsu,valor__exact = thora["valor__max"]).values('fecha')[:1]
        rrmaxh = thora["valor__max"]
        dic = {"rranual":str(rranual),"anioseco":str(minAnual),"aniolluvia":str(maxAnual),"fecAnioMax":str(fechaMaxAnual), "fecAnioMin":str(fechaMinAnual),
               "rrmes":str(rrmes), "messeco":str(rrSeco),"fmesSeco":fmeMin[0]['fecha'].strftime("%m/%d/%Y"),
                "rrlluvia":str(rrlluvia),"fmeslluvia":fmeMax[0]['fecha'].strftime("%m/%d/%Y"),
               "maxhora":str(rrmaxh),"fmaxhora":fhormax[0]['fecha'].strftime("%m/%d/%Y"),
               "dccl":str(dccl),"dcsl":str(dcsl),"Q10":str(cap10),"Q95":str(cap95)}
        return dic
    else:
        return None

def IndicaCaudal(estacion_id,inicio,fin,completo):

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
        print("Buscar segun las fechas")

    if amax is not None and amin and len(datos) > 2:
        iniconsu = datetime(amin, 1, 1, 0, 0, 0)
        finconsu = datetime(amax, 12, 31, 23, 59, 0)
        tcau = dia.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu, fecha__lte=finconsu).aggregate(Avg('valor'),Min('valor'), Max('valor'))
        camax = tcau["valor__max"]
        caavg = tcau["valor__avg"]
        camim = tcau["valor__min"]
        fdmax= dia.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu, fecha__lte=finconsu,
                                         valor__exact = tcau["valor__max"]).values('fecha')[:1]
        fdmin = dia.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu, fecha__lte=finconsu,
                                          valor__exact=tcau["valor__min"]).values('fecha')[:1]
        print("*****************************************")
        print(fdmax, fdmin)
        tcau = dia.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu, fecha__lte=finconsu).order_by("valor")
        total_count = tcau.count()

        p10 = posi(total_count,10)
        p50 = posi(total_count, 50)
        p95 = posi(total_count, 95)
        # print("posiciones",p10,p50,p95)
        cap10 = tcau[p10].valor
        cap50 = tcau[p50].valor
        cap95 = tcau[p95].valor
        cames = mes.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=iniconsu,
                                          fecha__lte=finconsu).aggregate(Avg('valor'),Min('valor'), Max('valor'))
        caSeco = cames["valor__min"]
        dic = {"cmax": str(round(camax,2)),"fdmax":fdmax[0]['fecha'].strftime("%m/%d/%Y"), "cavg": str(round(caavg, 2)), "cmim": str(round(camim,2)),
               "fdmin":fdmin[0]['fecha'].strftime("%m/%d/%Y"), "per10": str(round(cap10,2)), "per50":str(round(cap50,2)), "per95": str(round(cap95,2))
            ,"cmessec":str(round(caSeco,2))}
        return dic
    else:
        return None





def posi(N,i):
    x = (N*i)/100
    return int(x)

