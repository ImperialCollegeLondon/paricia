# -*- coding: utf-8 -*-
import json
import sys
from datetime import datetime, timedelta
from estacion.models import Estacion
from medicion.models import Medicion
from variable.models import Variable
from temporal.models import Datos
from vacios.models import Vacios
from formato.models import Clasificacion, Delimitador, Formato, Asociacion, Fecha, Hora
from marca.models import Marca
from django.db import connection
import time
from importacion.models import Importacion
from sedc.settings import BASE_DIR
from numbers import Number
import io


# consultar formatos por datalogger y estacion
def consultar_formatos(estacion):
    asociacion = list(Asociacion.objects.filter(est_id=estacion))
    lista = {}
    for item in asociacion:
        lista[item.for_id.for_id] = item.for_id.for_descripcion
    return lista


# guardar la informacion
def guardar_datos(imp_id, form):
    importacion = Importacion.objects.get(imp_id=imp_id)
    formato = importacion.for_id
    estacion = importacion.est_id
    # archivo a guardar
    print ('validar_fechas: ' + time.ctime())
    informacion, existe_vacio = validar_fechas(importacion)
    #archivo = open(str(BASE_DIR) + '/media/' + str(importacion.imp_archivo))
    ruta=str(BASE_DIR) + '/media/' + str(importacion.imp_archivo)
    enc = 'iso-8859-1'
    archivo=io.open(ruta, mode="r", encoding=enc)
    print ('checar sobreescribir y eliminar datos: ' + time.ctime())
    for fila in informacion:
        if fila.get('existe'):
            eliminar_datos(fila, importacion)
        if fila.get('vacio') and form.is_valid:
            observacion = form.cleaned_data['imp_observacion']
            guardar_vacios(fila, estacion, observacion, importacion.imp_fecha_ini)
    print ('construir_matriz: ' + time.ctime())
    datos = construir_matriz(archivo, formato, estacion)
    # print 'crear datos: '+time.ctime()
    Datos.objects.bulk_create(datos)
    print ('eliminar tabla datos' + time.ctime())
    Datos.objects.all().delete()
    importacion.imp_observacion = form.cleaned_data['imp_observacion']
    importacion.save()


def procesar_archivo_automatico(archivo, formato, estacion):
    datos = construir_matriz(archivo, formato, estacion)
    return datos


# leer el archivo y convertirlo a una matriz de objetos de la clase Datos
def construir_matriz(archivo, formato, estacion):
    # variables para el acumulado
    ValorReal = 0
    UltimoValor = 0
    # determinar si debemos restar 5 horas a la fecha del archivo
    cambiar_fecha = validar_datalogger(formato.mar_id)
    # validar si los valores del archivo son acumulados
    acumulado = validar_acumulado(formato.mar_id)
    clasificacion = list(Clasificacion.objects.filter(
        for_id=formato.for_id))
    i = 0
    datos = []
    lineas=archivo.readlines()
    for linea in lineas:
        i += 1
        # controlar la fila de inicio
        if i >= formato.for_fil_ini:
            valores = linea.split(formato.del_id.del_caracter)
            fecha = formato_fecha(formato, valores, cambiar_fecha)
            j = 0
            for fila in clasificacion:
                if fila.cla_valor is not None:
                    # valor=float(valores[fila.cla_valor])
                    valor = valid_number(valores[fila.cla_valor])
                    if valor != None:
                        if acumulado and fila.var_id.var_id == 1:
                            dblValor = valor
                            if dblValor == 0:
                                UltimoValor = 0
                            ValorReal = dblValor - UltimoValor
                            if ValorReal < 0:
                                ValorReal = dblValor
                            UltimoValor = dblValor
                            valor = ValorReal
                else:
                    valor = None
                if fila.cla_maximo is not None:
                    # maximo=float(valores[fila.cla_maximo])
                    maximo = valid_number(valores[fila.cla_maximo])
                else:
                    maximo = None
                if fila.cla_minimo is not None:
                    # minimo=float(valores[fila.cla_minimo])
                    minimo = valid_number(valores[fila.cla_minimo])
                else:
                    minimo = None
                dato = Datos(var_id=fila.var_id.var_id, est_id=estacion.est_id,
                             med_fecha=fecha, mar_id=formato.mar_id.mar_id,
                             med_valor=valor, med_maximo=maximo, med_minimo=minimo,
                             med_estado=True)
                datos.append(dato)
                j += 1
            if formato.for_tipo == 'automatico':
                formato.for_fil_ini = i + 1
                formato.save()
    return datos


# verficar vacios
def verificar_vacios(fecha_archivo, fecha_datos):
    estado = False
    vacios = []
    # fecha_datos=list(medicion)[0].get('med_fecha').date()
    if isinstance(fecha_datos, str):
        estado = False
    else:
        intervalo = timedelta(days=1)
        fecha_datos += intervalo
        if fecha_datos >= fecha_archivo:
            estado = False
        else:
            estado = True
    return estado


def guardar_vacios(informacion, estacion, observacion, fecha_archivo):
    variable = Variable.objects.get(var_id=informacion.get('var_id'))
    vacio = Vacios(est_id=estacion, var_id=variable,
                   vac_fecha_ini=informacion.get('ultima_fecha').date(),
                   vac_hora_ini=informacion.get('ultima_fecha').time(),
                   vac_fecha_fin=fecha_archivo.date(),
                   vac_hora_fin=fecha_archivo.time(),
                   vac_observacion=observacion)
    vacio.save()


def guardar_datos_automatico(datos):
    Datos.objects.bulk_create(datos)
    Datos.objects.all().delete()
    del datos[:]


# eliminar informacion en caso de existir
def eliminar_datos(informacion, importacion):
    fecha_ini = importacion.imp_fecha_ini
    fecha_fin = importacion.imp_fecha_fin
    fec_ini = str(fecha_ini)
    fec_fin = str(fecha_fin)
    year_ini = fecha_ini.strftime('%Y')
    year_fin = fecha_fin.strftime('%Y')
    est_id = str(importacion.est_id.est_id)
    var_cod = informacion.get('var_cod')
    if year_ini == year_fin:
        tabla = var_cod + '.m' + year_ini
        sql = 'DELETE FROM ' + tabla + ' WHERE '
        sql += 'est_id_id=' + str(est_id) + ' and '
        sql += 'med_fecha>=\'' + fec_ini + '\' and '
        sql += 'med_fecha<=\'' + fec_fin + '\''
        with connection.cursor() as cursor:
            cursor.execute(sql)
    else:
        range_year = range(int(year_ini), int(year_fin) + 1)
        for year in range_year:
            tabla = var_cod + '.m' + str(year)
            if str(year) == year_ini:
                sql = 'DELETE FROM ' + tabla + ' WHERE '
                sql += 'est_id_id=' + str(est_id) + ' and '
                sql += 'med_fecha>=\'' + fec_ini + '\''

            elif str(year) == year_fin:
                sql = 'DELETE FROM ' + tabla + ' WHERE '
                sql += 'est_id_id=' + str(est_id) + ' and '
                sql += 'med_fecha<=\'' + fec_fin + '\''

            else:
                sql = 'DELETE FROM ' + tabla + ' WHERE '
                sql += 'est_id_id=' + str(est_id)
            with connection.cursor() as cursor:
                cursor.execute(sql)


# validar si son datalogger VAISALA para restar 5 horas
def validar_datalogger(marca):
    if marca.mar_nombre == 'VAISALA':
        return True
    return False


def validar_acumulado(marca):
    if marca.mar_nombre == 'HOBO':
        return True
    return False


# convertir fecha y hora al formato adecuado
def formato_fecha(formato, valores, cambiar_fecha):
    if formato.for_col_fecha == formato.for_col_hora:
        separar = valores[formato.for_col_fecha].split(" ")
        fecha_str = separar[0]
        hora_str = separar[1]
        if len(separar) == 3:
            hora_str += ' ' + separar[2]
    else:
        fecha_str = valores[formato.for_col_fecha]
        hora_str = valores[formato.for_col_hora]
    fecha_str = fecha_str.strip('\"')
    hora_str = hora_str.strip('\"')
    try:
        fecha = datetime.strptime(fecha_str, formato.fec_id.fec_codigo)
    except ValueError:
        fecha = cambiar_formato_fecha(formato, fecha_str)
    try:
        hora = datetime.strptime(hora_str, formato.hor_id.hor_codigo)
    except ValueError:
        hora = cambiar_formato_hora(formato, hora_str)
    fecha_hora = datetime(fecha.year, fecha.month, fecha.day, hora.hour, hora.minute, hora.second)
    if cambiar_fecha:
        intervalo = timedelta(hours=5)
        fecha_hora -= intervalo
    return fecha_hora


def cambiar_formato_fecha(formato, fecha_str):
    con_fecha = list(Fecha.objects.exclude(fec_id=formato.fec_id.fec_id))
    for fila in con_fecha:
        try:
            fecha = datetime.strptime(fecha_str, fila.fec_codigo)
            formato.fec_id = fila
            formato.save()
            break
        except ValueError:
            pass
    return fecha


# busca un formato de hora para registro del archivo
def cambiar_formato_hora(formato, hora_str):
    con_hora = list(Hora.objects.exclude(hor_id=formato.hor_id.hor_id))
    for fila in con_hora:
        try:
            hora = datetime.strptime(hora_str, fila.hor_codigo)
            formato.hor_id = fila
            formato.save()
            break
        except ValueError:
            pass
    return hora


# verificar si existen los datos
def validar_fechas(importacion):
    print
    "validar_fechas" + time.ctime()
    fecha_ini = importacion.imp_fecha_ini
    fecha_fin = importacion.imp_fecha_fin
    formato = importacion.for_id
    estacion = importacion.est_id
    year = fecha_ini.strftime('%Y')
    year_fin = fecha_fin.strftime('%Y')
    fec_ini = str(fecha_ini)
    clasificacion = list(Clasificacion.objects.filter(
        for_id=formato.for_id))
    result = []
    existe_vacio = False
    for fila in clasificacion:
        var_cod = fila.var_id.var_codigo
        var_id = str(fila.var_id.var_id)
        est_id = str(estacion.est_id)
        tabla = var_cod + '.m' + year
        fecha_datos = ultima_fecha(est_id, var_cod, year_fin)
        existe_vacio = existe_vacio or verificar_vacios(fecha_ini, fecha_datos)
        resumen = {
            'var_id': fila.var_id.var_id,
            'var_cod': fila.var_id.var_codigo,
            'var_nombre': fila.var_id.var_nombre,
            'ultima_fecha': fecha_datos,
            'existe': consulta_fecha(fec_ini, est_id, tabla),
            'vacio': verificar_vacios(fecha_ini, fecha_datos)
        }
        result.append(resumen)
    return result, existe_vacio


def ultima_fecha(est_id, var_cod, year):
    print
    "ultima_fecha: " + time.ctime()
    # año base de la información
    year_int = 2007
    tabla = var_cod + '.m' + year
    while True:
        sql = 'SELECT med_id,med_fecha FROM ' + tabla
        sql += ' WHERE est_id_id=' + est_id + ' and med_estado is not False '
        sql += ' ORDER BY med_fecha DESC LIMIT 1'
        consulta = list(Medicion.objects.raw(sql))
        if len(consulta) > 0:
            informacion = consulta[0].med_fecha
            break
        else:
            year_int = int(year)
            year_int -= 1
            tabla = tabla = var_cod + '.m' + str(year_int)
            year = str(year_int)
        if year_int < 2016:
            break
    if len(consulta) <= 0:
        informacion = "No existen datos"
    return informacion


def consulta_fecha(fec_ini, est_id, tabla):
    print
    "consulta_fecha: " + time.ctime()
    sql = 'SELECT med_id FROM ' + tabla
    sql += ' WHERE med_fecha>= \'' + fec_ini + '\' '
    sql += 'and est_id_id=' + est_id + ' and med_estado is not False LIMIT 1'
    consulta = list(Medicion.objects.raw(sql))
    if len(consulta) > 0:
        return True
    return False


# obtener la fecha incial y final del archivo en base al formato
def get_fechas_archivo(archivo, formato, form):
    cambiar_fecha = validar_datalogger(formato.mar_id)
    datos = archivo.readlines()
    linea_ini = datos[formato.for_fil_ini - 1].decode("utf-8", "ignore")
    linea_fin = datos[len(datos) - 1].decode("utf-8", "ignore")
    print (type(linea_ini), type(formato.del_id.del_caracter))
    valores_ini = linea_ini.split(formato.del_id.del_caracter)
    print (type(valores_ini))
    valores_fin = linea_fin.split(formato.del_id.del_caracter)
    form.instance.imp_fecha_ini = formato_fecha(formato, valores_ini, cambiar_fecha)
    form.instance.imp_fecha_fin = formato_fecha(formato, valores_fin, cambiar_fecha)
    return form


def valid_number(val_str):
    val_num = None
    try:
        if isinstance(val_str, Number):
            val_num = float(val_str)
        elif val_str == "":
            val_num = None
        else:
            val_str.replace(",", ".")
            val_num = float(val_str)
    except:
        val_num = None
    return val_num
