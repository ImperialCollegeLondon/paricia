# -*- coding: utf-8 -*-
'''from formato.models import Formato,Asociacion
from importacion.functions import (
    procesar_archivo_automatico,guardar_datos_automatico)'''
import os
import shutil
from datetime import datetime

frecuencias = ['mn1', 'min2']


def run(*args):
    rootDir = '/Volumes/ftproot/PAPALLAC/'
    for dirName, subdirList, fileList in os.walk(rootDir, topdown=False):
        print('Found directory: %s' % dirName)
        for fname in fileList:
            # print('%s' % fname)
            if (buscar_archivo(fname, frecuencias[0])):
                print
                "llego"
                fecha_archivo(fname)
                archivo = open(rootDir + fname)
                linea = (archivo.readline()).split(',')
                print
                linea
                break


def buscar_archivo(fname, frecuencia):
    buscar = fname.find(frecuencia)
    # print type(buscar)
    if buscar >= 0:
        return True
    return False


# funcion para calcular la fecha y hora del archivo
def fecha_archivo(fname):
    print
    fname
    fecha_str = fname[12:24]
    fecha = datetime.strptime(fecha_str, '%y%m%d%H%M%S')
    print
    fecha_str, fecha
    return fecha


def move(src, dest):
    shutil.move(src, dest)


run()
