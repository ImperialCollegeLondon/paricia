# -*- coding: utf-8 -*-
from medicion.models import Medicion
from estacion.models import Estacion
from anuarios.models import PresionAtmosferica, HumedadSuelo, TemperaturaAgua, Caudal, NivelAgua
from django.db.models.functions import TruncMonth
from django.db.models import Max, Min, Avg, Count
from django.db.models.functions import (
    ExtractYear, ExtractMonth, ExtractDay, ExtractHour)


def matrizI(estacion, variable, periodo):
    datos = []
    obj_estacion = estacion.est_id.objects.get(est_id=estacion.est_id)
    consulta = Medicion.objects.filter(est_id=estacion.est_id) \
        .filter(var_id=variable.var_id).filter(med_fecha__year=periodo)
    if variable == "8":
        consulta = consulta.exclude(med_valor=0, med_maximo=0, med_minimo=0)
    consulta = consulta.annotate(month=TruncMonth('med_fecha')).values('month')
    med_max = list(consulta.annotate(maximo=Max('med_maximo'),
                                     valor=Max('med_valor')).values('maximo', 'valor').order_by('month'))
    med_min = list(consulta.annotate(minimo=Min('med_minimo'),
                                     valor=Min('med_valor')).values('minimo', 'valor').order_by('month'))
    med_avg = list(consulta.annotate(valor=Avg('med_valor'))
                   .values('valor', 'month').order_by('month'))
    maximos = []
    minimos = []
    promedios = []
    if variable.var_id == 6:
        for item_max, item_min, item_avg in zip(med_max, med_min, med_avg):
            obj_hsu = HumedadSuelo()
            obj_hsu.est_id = obj_estacion
            obj_hsu.hsu_periodo = periodo
            obj_hsu.hsu_mes = item_avg.get('month').month
            if item_max.get('maximo') is None:
                obj_hsu.hsu_maximo = round(item_max.get('valor'), 2)
            else:
                obj_hsu.hsu_maximo = round(item_max.get('maximo'), 2)
            if item_min.get('minimo') is None:
                obj_hsu.hsu_minimo = round(item_min.get('valor'), 2)
            else:
                obj_hsu.hsu_minimo = round(item_min.get('minimo'), 2)
            obj_hsu.hsu_promedio = round(item_avg.get('valor'), 2)
            datos.append(obj_hsu)
    elif variable.var_id == 8:
        for item_max, item_min, item_avg in zip(med_max, med_min, med_avg):
            obj_pat = PresionAtmosferica()
            obj_pat.est_id = obj_estacion
            obj_pat.pat_periodo = periodo
            obj_pat.pat_mes = item_avg.get('month').month
            if item_max.get('maximo') is None:
                obj_pat.pat_maximo = round(item_max.get('valor'), 2)
            else:
                obj_pat.pat_maximo = round(item_max.get('maximo'), 2)
            if item_min.get('minimo') is None:
                obj_pat.pat_minimo = round(item_min.get('valor'), 2)
            else:
                obj_pat.pat_minimo = round(item_min.get('minimo'), 2)
            obj_pat.pat_promedio = round(item_avg.get('valor'), 2)
            datos.append(obj_pat)
    elif variable.var_id == 9:
        for item_max, item_min, item_avg in zip(med_max, med_min, med_avg):
            obj_tag = TemperaturaAgua()
            obj_tag.est_id = obj_estacion
            obj_tag.tag_periodo = periodo
            obj_tag.tag_mes = item_avg.get('month').month
            if item_max.get('maximo') is None:
                obj_tag.tag_maximo = round(item_max.get('valor'), 2)
            else:
                obj_tag.tag_maximo = round(item_max.get('maximo'), 2)
            if item_min.get('minimo') is None:
                obj_tag.tag_minimo = round(item_min.get('valor'), 2)
            else:
                obj_tag.tag_minimo = round(item_min.get('minimo'), 2)
            obj_tag.tag_promedio = round(item_avg.get('valor'), 2)
            datos.append(obj_tag)
    elif variable.var_id == 10:
        for item_max, item_min, item_avg in zip(med_max, med_min, med_avg):
            obj_cau = Caudal()
            obj_cau.est_id = obj_estacion
            obj_cau.cau_periodo = periodo
            obj_cau.cau_mes = item_avg.get('month').month
            if item_max.get('maximo') is None:
                obj_cau.cau_maximo = round(item_max.get('valor'), 2)
            else:
                obj_cau.cau_maximo = round(item_max.get('maximo'), 2)
            if item_min.get('minimo') is None:
                obj_cau.cau_minimo = round(item_min.get('valor'), 2)
            else:
                obj_cau.cau_minimo = round(item_min.get('minimo'), 2)
            obj_cau.cau_promedio = round(item_avg.get('valor'), 2)
            datos.append(obj_cau)
    elif variable.var_id == 11:
        for item_max, item_min, item_avg in zip(med_max, med_min, med_avg):
            obj_nag = NivelAgua()
            obj_nag.est_id = obj_estacion
            obj_nag.nag_periodo = periodo
            obj_nag.nag_mes = item_avg.get('month').month
            if item_max.get('maximo') is None:
                obj_nag.nag_maximo = round(item_max.get('valor'), 2)
            else:
                obj_nag.nag_maximo = round(item_max.get('maximo'), 2)
            if item_min.get('minimo') is None:
                obj_nag.nag_minimo = round(item_min.get('valor'), 2)
            else:
                obj_nag.nag_minimo = round(item_min.get('minimo'), 2)
            obj_nag.nag_promedio = round(item_avg.get('valor'), 2)
            datos.append(obj_nag)
    return datos
