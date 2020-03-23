import horario.models as hor
import medicion.models as med
from django.db.models import Sum, Max, Min, Avg, Count
#from medicion.models import Precipitacion as mp, Caudal as mc
from estacion.models import Estacion
from datetime import datetime, timedelta
#
# SELECT id, estacion_id, fecha, valor, completo_mediciones, usado_para_diario
# FROM public.horario_precipitacion;
#
# select sum(valor) as valor from medicion_precipitacion where estacion = 1 and fecha > '2017-01-01 00:00:00' and fecha <= '2017-01-01 01:00:00' ;
#
# select * from estacion_estacion where est_externa = false and tipo_id in (1,2);
#
# select * from horario_precipitacion where estacion_id = 1 order by fecha desc limit 1;

def tohorarr():
    print("tohora function")
    estaciones = Estacion.objects.filter(tipo_id__in = (1,2), est_externa = False)
    #estaciones = Estacion.objects.filter(est_codigo ='M5021', est_externa=False)
    for e in estaciones:
        print(e)
        hora = hor.Precipitacion.objects.filter(estacion_id__exact = e.est_id).aggregate(Max('fecha'))
        #print(e.est_id, hora)
        if hora['fecha__max'] is not None: # condicion para cuando hay datos
            #print(hora[0].fecha)
            sumMedicionrr(e.est_id, hora['fecha__max'])
        else:# cuando no hay datos horarios
            print("todos los datos ")
            sumMedicionrr(e.est_id,None)

def sumMedicionrr(estacion, fechahorario):
    fechasMed = med.Precipitacion.objects.filter(estacion__exact= estacion).aggregate(Max('fecha'), Min('fecha'))


    if fechasMed['fecha__min'] != None and fechasMed['fecha__max'] != None :
        if fechahorario is not None:
            fechaTem = fechahorario + timedelta(hours=1)
        else:
            fechaTem = fechasMed['fecha__min']
        fmin = fechaTem
        print("fecha desde horarios ",fechahorario)
        print("fecha inicio de datos",fechasMed['fecha__min'],fechasMed['fecha__max'])
        while (fechaTem < fechasMed['fecha__max']):
            fechaTem = fechaTem + timedelta(hours=1)
            print("agregando datos  ",fmin, " - ",fechaTem)
            valor = med.Precipitacion.objects.filter(estacion__exact= estacion, fecha__gt=fmin,fecha__lte=fechaTem).aggregate(Sum('valor'))
            dthora = hor.Precipitacion()
            dthora.estacion_id = estacion
            dthora.fecha = fmin
            dthora.valor = valor['valor__sum']
            dthora.completo_mediciones=100
            dthora.usado_para_diario = False
            dthora.save()
            fmin = fechaTem
    else:
        print("no hay datos ")

##################

def tohoraca():
    print("tohora function")
    estaciones = Estacion.objects.filter(tipo_id__exact = 3, est_externa = False)
    #estaciones = Estacion.objects.filter(est_codigo ='M5021', est_externa=False)
    for e in estaciones:
        print(e)
        hora = hor.Caudal.objects.filter(estacion_id__exact = e.est_id).aggregate(Max('fecha'))
        #print(e.est_id, hora)
        if hora['fecha__max'] is not None: # condicion para cuando hay datos
            #print(hora[0].fecha)
            sumMedicionrr(e.est_id, hora['fecha__max'])
        else:# cuando no hay datos horarios
            print("todos los datos ")
            sumMedicionrr(e.est_id,None)

def sumMedicionca(estacion, fechahorario):
    fechasMed = med.Caudal.objects.filter(estacion__exact= estacion).aggregate(Max('fecha'), Min('fecha'))
    if fechasMed['fecha__min'] != None and fechasMed['fecha__max'] != None :
        if fechahorario is not None:
            fechaTem = fechahorario + timedelta(hours=1)
        else:
            fechaTem = fechasMed['fecha__min']
        fmin = fechaTem
        print("fecha desde horarios ",fechahorario)
        print("fecha inicio de datos",fechasMed['fecha__min'],fechasMed['fecha__max'])
        while (fechaTem < fechasMed['fecha__max']):
            fechaTem = fechaTem + timedelta(hours=1)
            print("agregando datos  ",fmin, " - ",fechaTem)
            valor = med.Caudal.objects.filter(estacion__exact= estacion, fecha__gt=fmin,fecha__lte=fechaTem).aggregate(Avg('valor'))
            dthora = hor.Caudal()
            dthora.estacion_id = estacion
            dthora.fecha = fmin
            dthora.valor = valor['valor__avg']
            dthora.completo_mediciones=100
            dthora.usado_para_diario = False
            dthora.save()
            fmin = fechaTem
    else:
        print("no hay datos ")

def run(*args):
    print(args)
    tohorarr()
    tohoraca()