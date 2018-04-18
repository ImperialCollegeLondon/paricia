# -*- coding: utf-8 -*-
from formato.models import Formato, Asociacion
from importacion.functions import (consultar_formatos, guardar_datos,
                                   procesar_archivo_automatico, guardar_vacios, guardar_datos_automatico)
import daemon
import time


def iniciar_lectura():
    try:
        formatos = list(Formato.objects.filter(for_tipo='automatico'))
        for formato in formatos:
            consulta = list(Asociacion.objects.filter(for_id=formato.for_id))
            if len(consulta) > 0:
                estacion = consulta[0].est_id
                archivo = open(formato.for_ubicacion + formato.for_archivo)
                datos = procesar_archivo_automatico(archivo, formato, estacion)
                archivo.close()
                if len(datos) > 0:
                    guardar_datos_automatico(datos)
                    registro = open('/tmp/sedc.txt', 'a')
                    registro.write(time.ctime() + ': Información guardada ' + str(estacion.est_codigo) + str(
                        formato.for_descripcion) + '\n')
                    registro.close()

                else:
                    registro = open('/tmp/sedc.txt', 'a')
                    registro.write(time.ctime() + ': No existe nueva informacion para el formato ' + str(
                        formato.for_descripcion) + '\n')
                    registro.close()
            else:
                registro = open('/tmp/sedc.txt', 'a')
                registro.write(time.ctime() + ': No existen formatos para iniciar la lectura' + '\n')
                registro.close()
                break
    except IOError as e:
        registro = open('/tmp/sedc.txt', 'a')
        registro.write(time.ctime() + ': El archivo no existe' + '\n')
        registro.close()
        pass
    # time.sleep(900)

    # guardar_datos(datos,variable)
