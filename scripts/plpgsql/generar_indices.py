# -*- coding: utf-8 -*-
from indices.models import EstPrecipitacion  as indPreci, EstCaudal as indCaudal
from diario.models import Precipitacion as diaPrecip, Caudal as diaCaudal
import numpy as np
from dateutil.relativedelta import relativedelta
import pandas as pd


def calculaIndicePrecip():
    estaciones = diaPrecip.objects.distinct('estacion_id').values('estacion_id')
    print(estaciones)

    for idest in estaciones:
        # fechas = diaPrecip.objects.order_by('estacion_id','fecha').distinct('estacion_id','fecha').values('estacion_id','fecha')
        print(idest, idest['estacion_id'])
        fechas = diaPrecip.objects.filter(estacion_id__exact=idest['estacion_id']).dates('fecha', 'month')
        print(type(fechas))
        cont = 0
        limit = len(fechas)
        for f in fechas:
            flimi = f + relativedelta(day=31)
            # print(f.strftime("%Y-%m-%d"), flimi)
            mes = pd.DataFrame.from_dict(
                diaPrecip.objects.filter(estacion_id__exact=idest['estacion_id'], fecha__gte=f.strftime("%Y-%m-%d"),
                                         fecha__lte=flimi.strftime("%Y-%m-%d")).values('fecha', 'valor'))


def run(*args):
    print(args)
    calculaIndicePrecip()

###python manage.py runscript generar_indices