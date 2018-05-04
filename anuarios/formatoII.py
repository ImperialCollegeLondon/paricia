# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import Precipitacion
from django.db.models.functions import TruncMonth
from django.db.models import Sum
from django.db.models.functions import (
    ExtractYear, ExtractMonth, ExtractDay, ExtractHour)


def matrizII(estacion, variable, periodo):
    datos = []
    obj_estacion = Estacion.objects.get(est_id=estacion.est_id)
    consulta = (Medicion.objects.filter(est_id=estacion.est_id)
                .filter(var_id=variable).filter(med_fecha__year=periodo)
                .annotate(month=TruncMonth('med_fecha')).values('month'))
    # valores de precipitación mensual
    med_mensual = list(consulta.annotate(suma=Sum('med_valor')).
                       values('suma', 'month').order_by('month'))
    datos_diarios = list(Medicion.objects
                         .filter(est_id=estacion.est_id)
                         .filter(var_id=variable)
                         .filter(med_fecha__year=periodo)
                         .annotate(month=ExtractMonth('med_fecha'), day=ExtractDay('med_fecha'))
                         .values('month', 'day')
                         .annotate(valor=Sum('med_valor'))
                         .values('valor', 'month', 'day').order_by('month', 'day'))
    max24H, maxdia, totdias = maximospre(datos_diarios)
    for item in med_mensual:
        obj_precipitacion = Precipitacion()
        obj_precipitacion.est_id = obj_estacion
        obj_precipitacion.pre_periodo = periodo
        obj_precipitacion.pre_mes = item.get('month').month
        obj_precipitacion.pre_suma = item.get('suma')
        obj_precipitacion.pre_maximo = max24H[item.get('month').month - 1]
        obj_precipitacion.pre_maximo_dia = maxdia[item.get('month').month - 1]
        obj_precipitacion.pre_dias = totdias[item.get('month').month - 1]
        datos.append(obj_precipitacion)
    return datos


def maximospre(datos_diarios):
    # retorna maxima precipitacion mensual y en que dia sucedio y cuantos dias hubo precipitacion
    max24H = []
    maxdia = []
    totdias = []

    for i in range(1, 13):
        val_max24h = []
        val_maxdia = []
        val_totdias = []
        for fila in datos_diarios:
            if fila.get('month') == i:
                val_max24h.append(fila.get('valor'))
                val_maxdia.append(fila.get('day'))
        # contar dias con lluvia en la variable count
        count = 0
        for j in val_max24h:
            if (j > 0):
                count += 1
        if len(val_max24h) > 0:
            max24H.append(max(val_max24h))
            maxdia.append(val_maxdia[val_max24h.index(max(val_max24h))])
        else:
            max24H.append(0)
            maxdia.append(0)
        totdias.append(count)
    return max24H, maxdia, totdias



