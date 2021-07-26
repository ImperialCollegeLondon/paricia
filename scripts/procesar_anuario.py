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

from anuarios import functions
from estacion.models import *
import datetime
from anuarios import functions as funanuario
def procesar():
    now = datetime.datetime.now()
    estaciones = Estacion.objects.all()
    #var = [1,2,3,4,5,6,7,8,9,10,11]
    var = [1,2,3,4,5,6,7,8,9,10,11]
    periodo = range(2000, (now.year - 1))
    print(periodo)
    for estacion in estaciones:
            for item in var:                
                for añio in periodo:
                    exists = funanuario.verficar_anuario(estacion, item, añio)
                    if exists == False:
                        datos = functions.calcular( estacion, item, añio )
                        template = functions.template(item)
                        exists = functions.verficar_anuario(estacion, item, añio)
                        functions.guardar_variable(datos, estacion, item, añio)
    print('listo')

procesar()