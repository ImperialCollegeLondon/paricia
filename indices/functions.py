from variable.models import Variable
import validacion.models as vali
import horario.models as hora
import diario.models as dia
import mensual.models as mes
from anuarios.models import Precipitacion, Caudal
from datetime import datetime, timedelta
from django.db.models import Sum, Max
from estacion.models import Estacion
import pandas as pd
import decimal

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
''' class acumEst():
    def __init__(self, fecha,valor,acum):
        self.fecha=fecha
        self.valor=valor
        self.acum=acum
    def __str__(self):
        return self.fecha.strftime("%m/%d/%Y, %H:%M:%S")+" "+str(self.valor)+" "+str(self.acum) '''

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
    print(data)
    return data



def anualizar(estacion_id):
    """une los datos mesuales generados por los anuarios en tablas anuales"""
    precip = Precipitacion.objects.filter(est_id__exact = estacion_id).order_by("pre_periodo","pre_mes")

    pass


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

def getCaudal(estacion_id,inicio, fin,frecuencia):
    """Calcula el caudal especifico de una estacion hidrológica"""
    print("funcion caudal ")
    const = 0.0
    est = Estacion.objects.get(est_id=estacion_id)
    inf = est.influencia_km
    print("influencia ",inf)
    #Qesp = Q / inf
    if frecuencia == 1:  # 'Horario':
        print("entra en horario frecuencia ",frecuencia)
        const = 0.0036
        caudal = hora.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                                 fecha__lte=fin).values( "valor")
    elif frecuencia == 2:  # 'Diario':
        print("entra en diario ",frecuencia)
        const = 0.0864
        caudal =  dia.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                                fecha__lte=fin).values( "valor")
    else:  # 'Mensual':
        print("entra en mensuales ,frecuencia")
        caudal = mes.Caudal.objects.filter(estacion_id__exact=estacion_id, fecha__gte=inicio,
                                                fecha__lte=fin).values('fecha','valor')
    valores = []

    if caudal is not None and len(caudal) > 0 and inf is not None:
        pand = pd.DataFrame(caudal)
        pand['CauEsp'] = pand['valor']/inf * decimal.Decimal(const)
        print(pand.head(5))
    return valores

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
