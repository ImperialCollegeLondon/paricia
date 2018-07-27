# -*- coding: utf-8 -*-
'''from formato.models import Formato,Asociacion
from importacion.functions import (
    procesar_archivo_automatico,guardar_datos_automatico)'''
import os
import shutil
from datetime import datetime, timedelta
from formato.models import Clasificacion, Formato, Asociacion
from importacion.functions import valid_number, validar_fechas, eliminar_datos
from importacion.models import Importacion
from home.models import Usuarios
import time
import daemon
from temporal.models import Datos
frecuencias = ['mn1', 'min2']

def run(*args):
    with daemon.DaemonContext():
        iniciar_lectura()

def iniciar_lectura():
    formatos = list(Formato.objects.filter(for_tipo='ftp'))
    if len(formatos)==0:
        registrar_log('No existen formatos FTP')
    while True:
        try:
            for formato in formatos:
                consulta = list(Asociacion.objects.filter(for_id=formato.for_id))
                print("for formatos")
                if len(consulta)>0:
                    estacion=consulta[0].est_id
                    registrar_log('Lectura Iniciada - Estacion:' + str(estacion.est_codigo) + ' Formato: ' + str(
                        formato.for_descripcion))
                    root_dir = formato.for_ubicacion
                    leer_archivos(root_dir,formato,estacion)
                else:

                    registrar_log('No existen formatos para iniciar la lectura')

                    break


        except IOError as e:
            registrar_log('El archivo no existe')
            print ("error")
            pass
            time.sleep(1500)



def registrar_log(mensaje):
    registro = open('/tmp/vaisala.txt', 'a')
    registro.write(time.ctime() + ': ' + mensaje + '\n')
    registro.close()

def get_ruta_backup(root_dir):
    ruta=root_dir.split("/")
    ruta_backup="/media/ftproot/respaldo/"+ruta[3]
    print(ruta_backup)
    return ruta_backup
# función para leer archivos correspondientes al formato y la estación
def leer_archivos(root_dir, formato, estacion):
    backup_dir = '/media/respaldo/COTOPAXI'
    for dir_name, subdir_list, file_list in os.walk(root_dir, topdown=False):
        print('Found directory: %s' % dir_name)
        for file_name in file_list:

            if buscar_archivo(file_name, formato.for_archivo):
                print('%s' % file_name)
                archivo = open(root_dir + file_name)
                fecha = fecha_archivo(file_name, formato.for_archivo)
                obj_importacion = set_object_importacion(estacion, formato, fecha, file_name)

                datos = procesar_archivo(archivo, formato, fecha, estacion)
                if len(datos)>0:

                    guardar_datos(obj_importacion, datos)
                    registrar_log('Información guardada Estacion:' + str(
                                estacion.est_codigo) + 'Formato:' + str(
                                formato.for_descripcion))
                    obj_importacion.save()
                    move(root_dir + file_name, get_ruta_backup(root_dir))
                    break
                else:
                    registrar_log('No existe nueva informacion para el Formato: '
                                  + str(formato.for_descripcion))
    return file_name

def guardar_datos(importacion, datos):
    informacion, existe_vacio = validar_fechas(importacion)
    for fila in informacion:
        if fila.get('existe'):
            print("eliminar información")
            eliminar_datos(fila, importacion)
    print("crear datos")
    Datos.objects.bulk_create(datos)
    Datos.objects.all().delete()


def buscar_archivo(file_name, frecuencia):
    buscar = file_name.find(frecuencia)
    if buscar >= 0:
        return True
    return False


def set_object_importacion(estacion, formato, fecha, archivo):
    intervalo = timedelta(minutes=15)
    usuario=Usuarios.objects.get(username='admin')
    importacion = Importacion()
    importacion.est_id = estacion
    importacion.for_id = formato
    importacion.imp_fecha_ini = fecha
    importacion.imp_fecha_fin = fecha + intervalo
    importacion.imp_archivo=archivo
    importacion.imp_observacion = 'Carga de Datos Automatica'
    importacion.usuario = usuario
    importacion.imp_tipo="a"
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
                print ("fecha", dato.med_fecha, "valor", dato.med_valor, "variable", dato.var_id)
                datos.append(dato)

            fecha += intervalo
        else:
            print("linea vacia")
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
