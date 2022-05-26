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

import random
from datetime import date, datetime, time, timedelta

from django.db import connection

from measurement.models import *


def llenarPrecipitacion():
    date_inicio = datetime(2020, 6, 1, 0, 0, 0)
    date_fin = datetime(2020, 8, 1, 0, 0, 0)
    date = date_inicio
    while date <= date_fin:
        date = date + timedelta(seconds=300)
        var4 = Var4Medicion(
            fecha=date,
            valor=random.randrange(0, 100),
            estacion_id=1,
            maximo=100,
            minimo=0,
        )
        var4.save()
        var5 = Var5Medicion(
            fecha=date,
            valor=random.randrange(0, 360),
            estacion_id=1,
            maximo=360,
            minimo=0,
        )
        var5.save()


def run():
    llenarPrecipitacion()
    print("Datos Generados e Ingresados")
