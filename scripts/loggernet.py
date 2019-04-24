# -*- coding: utf-8 -*-

from formato.models import Formato, Asociacion
from importacion.functions import ( eliminar_datos,
                                   guardar_vacios, construir_matriz,
                                   preformato_matriz, get_modelo,
                                   ultima_fecha, verificar_vacios)
from importacion.models import Importacion
from home.models import Usuarios
import time
import daemon
from temporal.models import Datos
from medicion.models import Precipitacion, TemperaturaAire, HumedadAire, VelocidadViento
from medicion.models import DireccionViento, HumedadSuelo, RadiacionSolar, PresionAtmosferica
from medicion.models import TemperaturaAgua, Caudal, NivelAgua
from numbers import Number


def run(*args):
    with daemon.DaemonContext():
        iniciar_lectura()


def iniciar_lectura():

    while True:
        formatos = list(Formato.objects.filter(for_tipo='automatico'))
        if len(formatos) == 0:
            registrar_log('No existen formatos lectura')
        try:
            for formato in formatos:
                consulta = list(Asociacion.objects.filter(for_id=formato.for_id))
                if len(consulta) > 0:
                    estacion = consulta[0].est_id
                    leer_archivos(formato, estacion)
                else:
                    registrar_log('No existen estaciones y formatos asociados')
        except IOError as e:
            registrar_log('Error: ' + str(e.errno) + ' ' + e.strerror)
            pass
        time.sleep(1500)


def registrar_log(mensaje):
    registro = open('/tmp/loggernet.txt', 'a')
    registro.write(time.ctime() + ': ' + mensaje + '\n')
    registro.close()


# función para leer archivos correspondientes al formato y la estación
def leer_archivos(formato, estacion):
    registrar_log('Lectura Iniciada Estacion:' + str(
        estacion.est_codigo) + 'Formato:' + str(
        formato.for_descripcion))
    try:
        archivo_src = formato.for_ubicacion + formato.for_archivo
        datos = preformato_matriz(archivo_src, formato)
    except Exception as e:
        registrar_log("No hay nueva información")
        datos = []
        pass
    except IOError as e:
        datos = []
        registrar_log('Error: ' + str(e.errno) + ' ' + e.strerror)
        pass

    if len(datos) > 0:
        # fecha_ini, fecha_fin = get_fechas_datos(datos)
        fecha_ini = datos.loc[0, 'fecha']
        fecha_fin = datos.loc[datos.shape[0] - 1, 'fecha']
        obj_importacion = set_object_importacion(estacion, formato, fecha_ini, fecha_fin, formato.for_archivo)
        matriz = construir_matriz(archivo_src, formato, estacion)
        guardar_datos(obj_importacion, matriz, estacion, formato)
        registrar_log('Información guardada Estacion:' + str(
                    estacion.est_codigo) + 'Formato:' + str(
                    formato.for_descripcion))
        obj_importacion.save()
    else:
        registrar_log('No existe nueva informacion para el Formato: '
                      + str(formato.for_descripcion))


def guardar_datos(importacion, datos, estacion, formato):
    observacion = 'vacio datos automaticos'
    flag = 0
    for var_id, tabla in datos.items():
        modelo = get_modelo(var_id)
        fecha_datos = ultima_fecha(modelo, estacion.est_id)
        if verificar_vacios(importacion.imp_fecha_ini, fecha_datos):
            registrar_log('Vacio de información')
            guardar_vacios(var_id, fecha_datos, estacion, observacion, importacion.imp_fecha_ini)
        eliminar_datos(modelo, importacion, estacion.est_id)

        modelo.objects.bulk_create(
            modelo(**row) for row in tabla.to_dict('records')
        )
        if flag == 0:
            formato.for_fil_ini = formato.for_fil_ini + tabla['fecha'].count()
            formato.save()
        flag+=1


def get_fechas_datos(datos):
    num_datos = len(datos) - 1
    fecha_ini = datos[0].med_fecha
    fecha_fin = datos[num_datos].med_fecha
    return fecha_ini, fecha_fin


def set_object_importacion(estacion, formato, fecha_ini, fecha_fin, archivo):
    usuario = Usuarios.objects.get(username='admin')
    importacion = Importacion()
    importacion.est_id = estacion
    importacion.for_id = formato
    importacion.imp_fecha_ini = fecha_ini
    importacion.imp_fecha_fin = fecha_fin
    importacion.imp_archivo = archivo
    importacion.imp_observacion = 'Carga de Datos Automatica'
    importacion.usuario = usuario
    importacion.imp_tipo = "a"
    return importacion



