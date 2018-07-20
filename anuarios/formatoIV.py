# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import HumedadAire
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import (
    ExtractYear, ExtractMonth, ExtractDay, ExtractHour)


def matrizIV(estacion, variable, periodo):
    datos = []
    consulta = Medicion.objects.filter(est_id=estacion.est_id) \
        .filter(var_id=variable.var_id).filter(med_fecha__year=periodo) \
        .annotate(month=TruncMonth('med_fecha')).values('month')
    consulta_max = (Medicion.objects.filter(est_id=estacion.est_id)
                    .filter(var_id=variable.var_id)
                    .filter(med_fecha__year=periodo).values('med_maximo').exists())

    datos_diarios_max = list(Medicion.objects
                             .filter(est_id=estacion.est_id)
                             .filter(var_id=variable.var_id)
                             .filter(med_fecha__year=periodo)
                             .exclude(med_valor=0)
                             .annotate(month=ExtractMonth('med_fecha'), day=ExtractDay('med_fecha'))
                             .values('month', 'day')
                             .annotate(maximo=Max('med_maximo'), valor=Max('med_valor'))
                             .values('maximo', 'valor', 'month', 'day').order_by('month', 'day'))
    datos_diarios_min = list(Medicion.objects
                             .filter(est_id=estacion.est_id)
                             .filter(var_id=variable.var_id)
                             .filter(med_fecha__year=periodo)
                             .exclude(med_valor=0)
                             .annotate(month=ExtractMonth('med_fecha'), day=ExtractDay('med_fecha'))
                             .values('month', 'day')
                             .annotate(minimo=Min('med_minimo'), valor=Min('med_valor'))
                             .values('minimo', 'valor', 'month', 'day').order_by('month', 'day'))

    med_avg = list(consulta.exclude(med_valor=0).
                   annotate(media=Avg('med_valor')).values('media', 'month').order_by('month'))
    maximo, maximo_dia = maximoshai(datos_diarios_max)
    minimo, minimo_dia = minimoshai(datos_diarios_min)
    for item in med_avg:
        mes = item.get('month').month
        obj_hai = HumedadAire()
        obj_hai.est_id = estacion
        obj_hai.hai_periodo = periodo
        obj_hai.hai_mes = mes
        obj_hai.hai_maximo = maximo[mes - 1]
        obj_hai.hai_maximo_dia = maximo_dia[mes - 1]
        obj_hai.hai_minimo = minimo[mes - 1]
        obj_hai.hai_minimo_dia = minimo_dia[mes - 1]
        obj_hai.hai_promedio = item.get('media')
        datos.append(obj_hai)
    return datos


def maximoshai(datos_diarios_max):
    # retorna maxima humedad mensual y en que dia sucedio
    max_abs = []
    maxdia = []
    for i in range(1, 13):
        val_max_abs = []
        val_maxdia = []
        for fila in datos_diarios_max:
            if fila.get('month') == i:
                if fila.get('maximo') is not None:
                    val_max_abs.append(fila.get('maximo'))
                elif fila.get('valor') is not None:
                    val_max_abs.append(fila.get('valor'))
                val_maxdia.append(fila.get('day'))
        if len(val_max_abs) > 0:
            max_abs.append(max(val_max_abs))
            maxdia.append(val_maxdia[val_max_abs.index(max(val_max_abs))])
        else:
            max_abs.append(0)
            maxdia.append(0)
    return max_abs, maxdia


def minimoshai(datos_diarios_min):
    # retorna minima humedad mensual y en que dia sucedio
    min_abs = []
    mindia = []
    for i in range(1, 13):
        val_min_abs = []
        val_mindia = []
        for fila in datos_diarios_min:
            if fila.get('month') == i:
                if fila.get('minimo') is not None:
                    val_min_abs.append(fila.get('minimo'))
                elif fila.get('valor') is not None:
                    val_min_abs.append(fila.get('valor'))
                val_mindia.append(fila.get('day'))

        if len(val_min_abs) > 0:
            min_abs.append(min(val_min_abs))
            mindia.append(val_mindia[val_min_abs.index(min(val_min_abs))])
        else:
            min_abs.append(0)
            mindia.append(0)
    return min_abs, mindia
