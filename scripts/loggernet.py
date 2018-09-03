# -*- coding: utf-8 -*-
import os
import shutil
from datetime import datetime, timedelta
from formato.models import Clasificacion, Formato, Asociacion
from importacion.functions import valid_number, validar_fechas, eliminar_datos, guardar_vacios, procesar_archivo_automatico
from importacion.models import Importacion
from home.models import Usuarios
import time
import daemon
from temporal.models import Datos


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
        archivo = open(formato.for_ubicacion + formato.for_archivo)
        datos = procesar_archivo_automatico(archivo, formato, estacion)
        archivo.close()
    except Exception as e:
        registrar_log("Error Inesperado "+ str(e.errno) + ' '+e.strerror)
        pass

    if len(datos) > 0:
        fecha_ini, fecha_fin = get_fechas_datos(datos)
        obj_importacion = set_object_importacion(estacion, formato, fecha_ini, fecha_fin, formato.for_archivo)
        guardar_datos(obj_importacion, datos, estacion)
        registrar_log('Información guardada Estacion:' + str(
                    estacion.est_codigo) + 'Formato:' + str(
                    formato.for_descripcion))
        obj_importacion.save()
    else:
        registrar_log('No existe nueva informacion para el Formato: '
                      + str(formato.for_descripcion))


def guardar_datos(importacion, datos, estacion):
    informacion, existe_vacio = validar_fechas(importacion)
    for fila in informacion:
        if fila.get('existe'):
            eliminar_datos(fila, importacion)
        if fila.get('vacio'):
            registrar_log('Vacio de información')
            observacion = 'vacio datos automaticos'
            guardar_vacios(fila, estacion, observacion, importacion.imp_fecha_ini)
    Datos.objects.bulk_create(datos)
    Datos.objects.all().delete()


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




#construir la matriz de datos
def procesar_archivo(archivo, formato, fecha, estacion):
    intervalo = timedelta(minutes=get_frecuencia(formato.for_archivo))
    lineas = archivo.readlines()
    clasificacion = list(Clasificacion.objects.filter(
        for_id=formato.for_id))
    datos = []
    for linea in lineas:
        valores = linea.split(',')
        if len(valores) > 1:
            val_lim = list(map(lambda item: item.strip(), valores))

            for fila in clasificacion:
                if fila.cla_valor is not None:
                    valor = valid_number(val_lim[fila.cla_valor])
                else:
                    valor = None
                if fila.cla_maximo is not None:
                    maximo = valid_number(val_lim[fila.cla_maximo])
                else:
                    maximo = None
                if fila.cla_minimo is not None:
                    minimo = valid_number(val_lim[fila.cla_minimo])
                else:
                    minimo = None
                dato = Datos(var_id=fila.var_id.var_id, est_id=estacion.est_id,
                             med_fecha=fecha, mar_id=formato.mar_id.mar_id,
                             med_valor=valor, med_maximo=maximo, med_minimo=minimo,
                             med_estado=True)
                datos.append(dato)

            fecha += intervalo
    return datos


def get_frecuencia(prefijo):
    frecuencia = 0
    if prefijo == "mn1":
        frecuencia = 1
    elif prefijo == "mn2":
        frecuencia=2
    return frecuencia


# funcion para calcular la fecha y hora del archivo
def fecha_archivo(file_name, prefijo):

    fecha_str = file_name[12:24]
    fecha = datetime.strptime(fecha_str, '%y%m%d%H%M%S')
    # resto 5horas por la diferencia del uso horario
    # y 15 minutos por la configuración del archivo
    frecuencia = get_frecuencia(prefijo)
    minuto = fecha.minute
    if frecuencia==2 and (minuto % 2)==0:
        intervalo = timedelta(hours=5, minutes=14)
    else:
        intervalo = timedelta(hours=5, minutes=15)
    fecha -= intervalo



    return fecha


def move(src, dest):
    shutil.move(src, dest)