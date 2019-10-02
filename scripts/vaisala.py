# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime, timedelta
from formato.models import Clasificacion, Formato, Asociacion
from importacion.functions import (validar_fechas, eliminar_datos, guardar_vacios,
                                   get_modelo, ultima_fecha, verificar_vacios, preformato_matriz,
                                   construir_matriz)
from importacion.models import Importacion
from home.models import Usuarios
import time
import daemon
from medicion.models import Precipitacion, TemperaturaAire, HumedadAire, VelocidadViento
from medicion.models import DireccionViento, HumedadSuelo, RadiacionSolar, PresionAtmosferica
from medicion.models import TemperaturaAgua, Caudal, NivelAgua

from numbers import Number

import pandas.io.common
from django.db.utils import DataError

def run(*args):
    with daemon.DaemonContext():
        iniciar_lectura()


def iniciar_lectura():

    while True:
        formatos = list(Formato.objects.filter(for_tipo='ftp'))
        # print(formatos)
        if len(formatos) == 0:
            registrar_log('No existen formatos FTP')
        try:
            for formato in formatos:
                consulta = list(Asociacion.objects.filter(for_id=formato.for_id))
                if len(consulta) > 0:
                    estacion = consulta[0].est_id
                    root_dir = formato.for_ubicacion
                    leer_archivos(root_dir, formato, estacion)
                    respaldar_archivos(root_dir)
                else:
                    registrar_log('No existen formatos para iniciar la lectura')

        except IOError as e:
            registrar_log('Error: ' + str(e.errno) + ' ' + e.strerror)
            pass

        time.sleep(1500)


def respaldar_archivos(root_dir):
    for dir_name, subdir_list, file_list in os.walk(root_dir, topdown=False):
        for file_name in file_list:
            # mn5 = buscar_archivo(file_name, 'mn5')
            mn1 = buscar_archivo(file_name, 'mn1')
            mn2 = buscar_archivo(file_name, 'mn2')
            hor = buscar_archivo(file_name, 'hor')
            dia = buscar_archivo(file_name, 'dia')
            if hor or dia or mn1 or mn2:
                move(root_dir + file_name, get_ruta_backup(root_dir))
            else:
                registrar_log('No existen archivos nuevos')


def registrar_log(mensaje):
    registro = open('/tmp/vaisala.txt', 'a')
    registro.write(time.ctime() + ': ' + mensaje + '\n')
    registro.close()


def get_ruta_backup(root_dir):
    ruta = root_dir.split("/")
    ruta_backup = "/media/ftproot/respaldo/"+ruta[3]
    # ruta_backup = "/media/respaldo/COTOPAXI/"
    return ruta_backup


# función para leer archivos correspondientes al formato y la estación
def leer_archivos(root_dir, formato, estacion):
    for dir_name, subdir_list, file_list in os.walk(root_dir, topdown=False):
        for file_name in file_list:
            '''if buscar_archivo(file_name, formato.for_archivo):
                archivo = open(root_dir + file_name)
                fecha = fecha_archivo(file_name, formato.for_archivo)
                obj_importacion = set_object_importacion(estacion, formato, fecha, file_name, formato.for_archivo)
                registrar_log('Lectura Iniciada Estacion:' + str(
                    estacion.est_codigo) + ' archivo: ' + file_name)
                datos = procesar_archivo(archivo, formato, fecha, estacion)
                archivo.close()
                if len(datos) > 0:
                    guardar_datos(obj_importacion, datos, estacion)
                    registrar_log('Información guardada Estacion:' + str(
                                estacion.est_codigo) + ' Archivo: ' + str(
                                file_name))
                    obj_importacion.save()
                    move(root_dir + file_name, get_ruta_backup(root_dir))
                else:
                    registrar_log('No existe información en el archivo: '
                                  + str(file_name))
            else:
                registrar_log('No hay nueva información en el directorio FTP. Estacion: '+str(
                                estacion.est_codigo))'''
            # print(formato.for_archivo)
            if formato.for_archivo == 'YDOC':
                procesar_ydoc(file_name, root_dir, formato, estacion)
            else:
                procesar_vaisala(file_name, root_dir, formato, estacion)


def procesar_vaisala(file_name, root_dir, formato, estacion):
    if buscar_archivo(file_name, formato.for_archivo):
        archivo = open(root_dir + file_name)
        fecha = fecha_archivo(file_name, formato.for_archivo)
        obj_importacion = set_object_importacion(estacion, formato, fecha, file_name, formato.for_archivo)
        registrar_log('Lectura Iniciada Estacion:' + str(
            estacion.est_codigo) + ' archivo: ' + file_name)
        datos = procesar_archivo(archivo, formato, fecha, estacion)
        archivo.close()
        if len(datos) > 0:
            guardar_datos(obj_importacion, datos, estacion,formato)
            registrar_log('Información guardada Estacion:' + str(
                estacion.est_codigo) + ' Archivo: ' + str(
                file_name))
            obj_importacion.save()
            move(root_dir + file_name, get_ruta_backup(root_dir))
        else:
            registrar_log('No existe información en el archivo: '
                          + str(file_name))
    else:
        registrar_log('No hay nueva información en el directorio FTP. Estacion: ' + str(
            estacion.est_codigo))


def procesar_ydoc(file_name, root_dir, formato, estacion):
    archivo = root_dir + file_name
    registrar_log('Lectura Iniciada Estacion:' + str(
        estacion.est_codigo) + ' archivo: ' + file_name)
    try:
        datos = preformato_matriz(archivo, formato)
    except pandas.io.common.EmptyDataError:
        registrar_log('No existe nueva informacion para el Formato: '
                      + str(formato.for_descripcion))
        datos = []
        pass
    except Exception as e:
        registrar_log("Error Inesperado:"+str(e))
        datos = []
        pass
    except IOError as e:
        datos = []
        registrar_log('Error: ' + str(e.errno) + ' ' + e.strerror)
        pass
    except DataError as e:
        datos = []
        registrar_log('Error: ' + str(e.errno) + ' ' + e.strerror)
        pass
    # print(datos)
    # print(len(datos))
    if len(datos) > 0:
        # fecha_ini, fecha_fin = get_fechas_datos(datos)
        fecha_ini = datos.loc[0, 'fecha']
        fecha_fin = datos.loc[datos.shape[0] - 1, 'fecha']
        obj_importacion = set_object_importacion_ydoc(estacion, formato, fecha_ini, fecha_fin, formato.for_archivo)
        matriz = construir_matriz(archivo, formato, estacion)
        # print(matriz)
        try:
            guardar_datos(obj_importacion, matriz, estacion, formato)
            registrar_log('Información guardada Estacion:' + str(
                        estacion.est_codigo) + 'Formato:' + str(
                        formato.for_descripcion))
            obj_importacion.save()
        except DataError:
            registrar_log('Error en la información')
        except TypeError:
            registrar_log('Error en la información')
        except ValueError:
            registrar_log('Error en la información')
        move(root_dir + file_name, get_ruta_backup(root_dir))


def guardar_datos(importacion, datos, estacion, formato):
    observacion = 'vacio datos automaticos'

    for var_id, tabla in datos.items():
        modelo = get_modelo(var_id)
        fecha_datos = ultima_fecha(modelo, estacion.est_id)
        if verificar_vacios(importacion.imp_fecha_ini, fecha_datos):
            registrar_log('Vacio de información')
            guardar_vacios(var_id, fecha_datos, estacion, observacion, importacion.imp_fecha_ini)
        eliminar_datos(modelo, importacion, estacion.est_id)
        if formato.for_archivo == 'YDOC':
            modelo.objects.bulk_create(
                modelo(**row) for row in tabla.to_dict('records')
            )
        else:
            modelo.objects.bulk_create(tabla)



def buscar_archivo(file_name, frecuencia):
    buscar = file_name.find(frecuencia)
    if buscar >= 0:
        return True
    return False


def set_object_importacion(estacion, formato, fecha, archivo, prefijo):
    frecuencia = get_frecuencia(prefijo)
    if frecuencia == 5:
        intervalo = timedelta(minutes=15)
    usuario = Usuarios.objects.get(username='admin')
    importacion = Importacion()
    importacion.est_id = estacion
    importacion.for_id = formato
    importacion.imp_fecha_ini = fecha
    importacion.imp_fecha_fin = fecha + intervalo
    importacion.imp_archivo = archivo
    importacion.imp_observacion = 'Carga de Datos Automatica'
    importacion.usuario = usuario
    importacion.imp_tipo = "a"
    return importacion


def set_object_importacion_ydoc(estacion, formato, fecha_ini, fecha_fin, archivo):
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


# construir la matriz de datos
def procesar_archivo(archivo, formato, fecha, estacion):
    intervalo = timedelta(minutes=get_frecuencia(formato.for_archivo))
    lineas = archivo.readlines()
    clasificacion = list(Clasificacion.objects.filter(
        for_id=formato.for_id))

    datos_variables = {}
    for fila in clasificacion:
        fecha_datos = fecha
        modelo = get_modelo(fila.var_id.var_id)
        datos = []
        for linea in lineas:
            valores = linea.split(',')
            if len(valores) > 1:
                # quitar los espacios de los valores del archivo
                val_lim = list(map(lambda item: item.strip(), valores))

                if fila.cla_valor is not None and fila.cla_valor <= len(val_lim):
                    valor = valid_number(val_lim[fila.cla_valor-1], fila.var_id.var_id)
                else:
                    valor = None
                if fila.cla_maximo is not None and fila.cla_maximo <= len(val_lim):
                    maximo = valid_number(val_lim[fila.cla_maximo-1], fila.var_id.var_id)
                else:
                    maximo = None

                if fila.cla_minimo is not None and fila.cla_minimo <= len(val_lim):
                    minimo = valid_number(val_lim[fila.cla_minimo-1], fila.var_id.var_id)
                else:
                    minimo = None
                if fila.var_id.var_id == 1:
                    dato = modelo(estacion=estacion.est_id, fecha=fecha_datos, valor=valor)
                else:
                    dato = modelo(estacion=estacion.est_id, fecha=fecha_datos, valor=valor,
                                  maximo=maximo, minimo=minimo)
                datos.append(dato)

            fecha_datos += intervalo
        datos_variables[fila.var_id.var_id] = datos

    return datos_variables


def get_frecuencia(prefijo):
    frecuencia = 0
    if prefijo == "mn1":
        frecuencia = 1
    elif prefijo == "mn2":
        frecuencia = 2
    elif prefijo == "mn5":
        frecuencia = 5
    return frecuencia


# funcion para calcular la fecha y hora del archivo
def fecha_archivo(file_name, prefijo):
    fecha_str = file_name[12:24]
    fecha = datetime.strptime(fecha_str, '%y%m%d%H%M%S')
    # resto 5horas por la diferencia del uso horario
    # y 15 minutos por la configuración del archivo
    frecuencia = get_frecuencia(prefijo)
    minuto = fecha.minute
    if frecuencia == 2 and (minuto % 2) == 0:
        intervalo = timedelta(hours=5, minutes=14)
    else:
        intervalo = timedelta(hours=5, minutes=15)
    fecha -= intervalo

    return fecha


def valid_number(val_str, var_id):
    val_num = None
    try:
        if len(val_str) >= 10:
            val_num = None
        elif isinstance(val_str, Number):
            val_num = float(val_str)
            val_num = round(val_num, 3)
        elif val_str == "":
            val_num = None
        else:
            val_str.replace(",", ".")
            val_num = float(val_str)
            val_num = round(val_num, 3)
        if val_num is not None:
            if var_id == 7 and val_num > 1400:
                val_num = 1400
    except:
        val_num = None
    return val_num


def move(src, dest):
    try:
        shutil.move(src, dest)
    except:
        registrar_log('Error de copia al respaldo archivo existente')
        pass


# iniciar_lectura()

