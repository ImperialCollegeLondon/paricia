import pandas as pd
from estacion.models import Estacion
from cruce.models import Cruce
from importacion.functions import get_modelo
import time
import daemon
from home.functions import dictfetchall
from medicion.models import Precipitacion, TemperaturaAire, HumedadAire, VelocidadViento
from medicion.models import DireccionViento, HumedadSuelo, RadiacionSolar, PresionAtmosferica
from medicion.models import TemperaturaAgua, Caudal, NivelAgua

from validacion.models import Precipitacion as PRE
from validacion.models import TemperaturaAire as TAI
from validacion.models import HumedadAire as HAI
from validacion.models import VelocidadViento as VVI
from validacion.models import DireccionViento as DVI
from validacion.models import HumedadSuelo as HSU
from validacion.models import RadiacionSolar as RAD
from validacion.models import PresionAtmosferica as PAT
from validacion.models import TemperaturaAgua as TAG
from validacion.models import Caudal as CAU
from validacion.models import NivelAgua as NAG


'''def run(*args):
    with daemon.DaemonContext():
        iniciar_lectura()'''


def registrar_log(mensaje):

    registro = open('/home/developer/log_sedc/datoscrudos.txt', 'a')
    registro.write(time.ctime() + ': ' + mensaje + '\n')

    registro.close()


def iniciar_lectura():
    #estaciones = Estacion.objects.filter(est_externa=False).filter(est_id=13)
    # Humedad del Aire, Velocidad y Dirección del Viento
    #filtro_estaciones = [1, 5, 6, 7, 8, 9, 11, 12, 13]
    # Humedad del Suelo y Radiación Solar
    #filtro_estaciones = [8, 9, 11, 12, 13]
    # Presión Atmosférica
    #filtro_estaciones = [1, 5, 6, 7]
    # Temperatura del Agua, Caudal, Nivel del Agua
    #filtro_estaciones = [17]

    # filtro_estaciones = [21]
    filtro_estaciones = [29, 30, 31, 32]

    #estaciones = Estacion.objects.filter(est_externa=False).exclude(est_id__in=filtro_estaciones)
    estaciones = Estacion.objects.filter(est_id__in=filtro_estaciones)
    #estaciones = Estacion.objects.filter(est_externa=False).all()


    #periodos = [2015, 2016, 2017, 2018]
    periodos = [2013, 2014, 2015, 2016, 2017, 2018]



    for fila_est in estaciones:

        cruces = Cruce.objects.filter(est_id=fila_est.est_id)
        for fila_cru in cruces:

            modelo_validacion = globals()[fila_cru.var_id.var_codigo]

            modelo_medicion = get_modelo(fila_cru.var_id.var_id)


            filtro = [10]


            if fila_cru.var_id.var_id in filtro:

                for periodo in periodos:
                    datos_crudos = modelo_medicion.objects.filter(estacion_id=fila_est.est_id).filter(fecha__year=periodo)

                    if len(datos_crudos) > 0:

                        datos_validacion = []
                        for dato in datos_crudos:
                            objeto_validacion = modelo_validacion(
                                estacion_id=dato.estacion_id, fecha=dato.fecha, valor=dato.valor,
                                usado_para_horario=False, validacion=0
                            )
                            datos_validacion.append(objeto_validacion)
                            # print(datos_validacion[0].validacion)
                            # print(dato.estacion)
                        # print(datos_validacion)

                        modelo_validacion.objects.bulk_create(datos_validacion)
                        '''registrar_log(
                            "Estacion: " + fila_est.est_codigo +
                            "; Variable: " + fila_cru.var_id.var_nombre +
                            "; Num Datos: " + str(len(datos_crudos)))'''


iniciar_lectura()

