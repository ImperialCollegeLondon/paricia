# -*- coding: utf-8 -*-


from datetime import datetime, timedelta
from variable.models import Variable
from temporal.models import Datos
from vacios.models import Vacios
from formato.models import Clasificacion, Asociacion, Fecha, Hora
# from marca.models import Marca
# from django.db import connection
# import time
from medicion.models import Precipitacion, TemperaturaAire, HumedadAire, VelocidadViento
from medicion.models import DireccionViento, HumedadSuelo, RadiacionSolar, PresionAtmosferica
from medicion.models import TemperaturaAgua, Caudal, NivelAgua
from importacion.models import Importacion,ImportacionTemp
from sedc.settings import BASE_DIR
from numbers import Number
from django.db import connection, transaction
import io
import pandas as pd
import numpy as np
import shutil
import os


unix_epoch = np.datetime64(0, 's')
one_second = np.timedelta64(1, 's')


# consultar formatos por datalogger y estacion
def consultar_formatos(estacion):
    asociacion = list(Asociacion.objects.filter(est_id=estacion, for_id__for_tipo='convencional'))
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
    # print ('validar_fechas: ' + time.ctime())
    informacion, existe_vacio = validar_fechas(importacion)
    ruta = str(BASE_DIR) + '/media/' + str(importacion.imp_archivo)
    enc = 'iso-8859-1'
    archivo = io.open(ruta, mode="r", encoding=enc)
    # print ('checar sobreescribir y eliminar datos: ' + time.ctime())
    for fila in informacion:
        if fila.get('existe'):
            eliminar_datos(fila, importacion)
        if fila.get('vacio') and form.is_valid:
            observacion = form.cleaned_data['imp_observacion']
            guardar_vacios(fila, estacion, observacion, importacion.imp_fecha_ini)
    # print ('construir_matriz: ' + time.ctime())
    datos = construir_matriz(archivo, formato, estacion)
    Datos.objects.bulk_create(datos)
    # print ('eliminar tabla datos' + time.ctime())
    Datos.objects.all().delete()
    importacion.imp_observacion = form.cleaned_data['imp_observacion']
    importacion.save()


# verificar si la columna de la hora y fecha tienen el formato adecuado
def verificar_fechahora(fechahora, formatofechahora):
    if isinstance(fechahora, datetime):
        return fechahora
    elif isinstance(fechahora, np.datetime64):
        fechahora = datetime.utcfromtimestamp((fechahora - unix_epoch) / one_second)
        return fechahora
    elif isinstance(fechahora, str):
        pass
        # valores = fechahora.split(" ")
        # valores = list(filter(None, valores))
        # fechahora_str = valores[0].strip('\"') + ' ' + valores[1].strip('\"')

    elif isinstance(fechahora, list):
        fechahora = ' '.join(fechahora)

    elif isinstance(fechahora, pd.Series):
        fechahora = ' '.join([str(val) for val in list(fechahora[:])])

    else:
        fechahora = ''

    try:
        _fechahora = datetime.strptime(fechahora, formatofechahora)
    except:
        _fechahora = None
    return _fechahora


# Obtener los datos del archivo importado
def preformato_matriz(archivo_src, formato):
    skipfooter = 0
    if formato.for_fil_cola:
        skipfooter = formato.for_fil_cola
    if formato.ext_id.ext_valor in ['XLSX', 'XLS']:
        archivo = pd.read_excel(archivo_src, header=None,
                                skiprows=formato.for_fil_ini-1, skipfooter=skipfooter,
                                error_bad_lines=False)
    else:
        # TODO chequear opciones: sep, delim
        if formato.del_id.del_caracter == ' ':
            archivo = pd.read_csv(archivo_src, delim_whitespace=True, header=None,
                                  skiprows=formato.for_fil_ini-1, skipfooter=skipfooter,
                                  encoding="ISO-8859-1", error_bad_lines=False)
        else:
            archivo = pd.read_csv(archivo_src, sep=formato.del_id.del_caracter, header=None,
                                  skiprows=formato.for_fil_ini-1, skipfooter=skipfooter,
                                  encoding="ISO-8859-1", error_bad_lines=False)

    formatofechahora = formato.fec_id.fec_codigo + ' ' + formato.hor_id.hor_codigo
    if formato.for_col_fecha == formato.for_col_hora:
        print("llego al true")
        # TODO añadir column from a array para evitar usar pd.Series y que tenga TYPE DATETIMTE.DATETIME
        archivo['fecha'] = pd.Series([verificar_fechahora(row, formatofechahora) for row in archivo[formato.for_col_fecha - 1].values], index=archivo.index)
    else:
        print("llego al false")
        items_fecha = formato.fec_id.fec_codigo.split(formato.del_id.del_caracter)
        cols_fecha = list(range(formato.for_col_fecha - 1, formato.for_col_fecha - 1 + len(items_fecha)))
        items_hora = formato.hor_id.hor_codigo.split(formato.del_id.del_caracter)
        cols_hora = list(range(formato.for_col_hora - 1, formato.for_col_hora - 1 + len(items_hora)))
        cols = cols_fecha + cols_hora
        # TODO añadir column from a array para evitar usar pd.Series y que tenga TYPE DATETIMTE.DATETIME
        archivo['fechahora_str'] = pd.Series([' '.join(row.astype(str)) for row in archivo[cols].values], index=archivo.index)
        archivo['fecha'] = pd.Series([verificar_fechahora(row, formatofechahora) for row in archivo['fechahora_str'].values], index=archivo.index)
    cambiar_fecha = validar_datalogger(formato.mar_id)
    if cambiar_fecha:
        intervalo = timedelta(hours=5)
        archivo['fecha'] = archivo['fecha'] - intervalo
    archivo = archivo.sort_values('fecha')
    archivo = archivo.reset_index(drop=True)
    return archivo


# Esta funcion pasa la importación temporal a final
def guardar_datos__temp_a_final(imp_id, form):
    importaciontemp = ImportacionTemp.objects.get(imp_id=imp_id)
    formato = importaciontemp.for_id
    estacion = importaciontemp.est_id
    ruta = str(BASE_DIR) + '/media/' + str(importaciontemp.imp_archivo)
    datos = construir_matriz(ruta, formato, estacion)
    observacion = form.cleaned_data['imp_observacion']
    for var_id, tabla in datos.items():

        varmodel = get_modelo(var_id)
        fecha_datos = ultima_fecha(varmodel, estacion.est_id)
        if verificar_vacios(importaciontemp.imp_fecha_ini, fecha_datos):
            guardar_vacios(var_id, fecha_datos, estacion, observacion, importaciontemp.imp_fecha_ini)
        eliminar_datos(varmodel, importaciontemp, estacion.est_id)
        varmodel.objects.bulk_create(
            varmodel(**row) for row in tabla.to_dict('records')
        )

    ruta_final = str(importaciontemp.imp_archivo).replace('archivos/tmp/','archivos/')
    ruta_final_full = str(BASE_DIR) + '/media/' + ruta_final
    shutil.copy(ruta, ruta_final_full)
    importacion = Importacion(
        est_id=importaciontemp.est_id,
        for_id=importaciontemp.for_id,
        imp_fecha=importaciontemp.imp_fecha,
        imp_fecha_ini=importaciontemp.imp_fecha_ini,
        imp_fecha_fin=importaciontemp.imp_fecha_fin,
        imp_archivo=ruta_final,
        imp_observacion=observacion,
        usuario=importaciontemp.usuario
    )
    ruta_original_full = str(BASE_DIR) + '/media/' + str(importaciontemp.imp_archivo)
    with transaction.atomic():
        importacion.save()
        importaciontemp.delete()
    os.remove(ruta_original_full)
    return importacion.imp_id


# leer el archivo y convertirlo a una matriz de objetos de la clase Datos
'''def construir_matriz(archivo, formato, estacion):
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
                    valor = valid_number(valores[fila.cla_valor], fila.var_id.var_id)
                    if valor != None and acumulado and fila.var_id.var_id == 1:
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
                    maximo = valid_number(valores[fila.cla_maximo], fila.var_id.var_id)
                else:
                    maximo = None
                if fila.cla_minimo is not None:
                    minimo = valid_number(valores[fila.cla_minimo], fila.var_id.var_id)
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
    return datos'''


def construir_matriz(archivo_src, formato, estacion):
    # TODO : Eliminar validar_datalogger, validar acumulado

    # Preformato entrega matriz ordenada por fecha
    matriz = preformato_matriz(archivo_src, formato)
    fecha_ini = matriz.loc[0, 'fecha']
    fecha_fin = matriz.loc[matriz.shape[0] - 1, 'fecha']

    clasificacion = list(Clasificacion.objects.filter(for_id=formato.for_id))
    datos_variables = {}
    for var in clasificacion:
        columnas = []
        columnas.append(('fecha', 'fecha'))
        ##
        columnas.append((var.cla_valor - 1, 'valor'))
        if var.col_validador_valor:
            matriz.loc[matriz[var.col_validador_valor - 1] != var.txt_validador_valor, var.cla_valor - 1] = np.nan
        ##
        if var.cla_maximo:
            columnas.append((var.cla_maximo - 1, 'maximo'))
        if var.col_validador_maximo:
            matriz.loc[matriz[var.col_validador_maximo - 1] != var.txt_validador_maximo, var.cla_maximo - 1] = np.nan
        ##
        if var.cla_minimo:
            columnas.append((var.cla_minimo - 1, 'minimo'))
        if var.col_validador_minimo:
            matriz.loc[matriz[var.col_validador_minimo - 1] != var.txt_validador_minimo, var.cla_minimo - 1] = np.nan
        ##
        datos = matriz.loc[:, [v[0] for v in columnas]]
        datos.rename(columns=dict(columnas), inplace=True)

        for col in datos:
            if col == 'fecha':
                continue

            if var.coma_decimal:
                datos[col] = pd.Series([numero_coma_decimal(val) for val in datos[col].values], index=matriz.index)
            else:
                datos[col] = pd.Series([numero_punto_decimal(val) for val in datos[col].values], index=matriz.index)

        # Eliminar NAs
        columnas_datos = [columna[1] for columna in columnas if columna[1]!='fecha']
        datos = datos.dropna(axis=0, how='all', subset=columnas_datos)

        # modificar valores de Radiacion mayores a 1400
        if var.var_id_id == 7:
            datos.loc[datos['valor'] > 1400, 'valor'] = 1400

        if var.acumular:
            # Se asume que si es incremental solo trabaja con VALOR (Se excluye MAXIMO y MINIMO)
            if var.incremental:
                datos['valor'] = datos['valor'].diff()
                # datos['valor'][datos['valor'] < 0] = np.nan
                datos.loc[datos['valor'] < 0, 'valor'] = np.nan
                datos=datos.dropna()
            datos['fecha'] = datos['fecha'].apply(lambda x: x.replace(minute=int(x.minute/5) * 5, second=0, microsecond=0, nanosecond=0) )
            datos['fecha'] = datos['fecha'] + pd.Timedelta(minutes=5)
            cuenta = datos.groupby('fecha')['valor'].sum().to_frame()
            datos = cuenta['valor'] * float(var.resolucion)

            fecha_ini = fecha_ini.replace(minute=int(fecha_ini.minute/5) * 5, second=0, microsecond=0, nanosecond=0) + pd.Timedelta(minutes=5)
            fecha_fin = fecha_fin.replace(minute=int(fecha_fin.minute/5) * 5, second=0, microsecond=0, nanosecond=0) + pd.Timedelta(minutes=5)
            tabla = pd.date_range(fecha_ini, fecha_fin, freq='5min', name='fecha').to_frame()
            datos = pd.concat([tabla, datos], axis=1)
            datos = datos.fillna(0)
        else:
            if var.incremental:
                datos['valor'] = datos['valor'].diff()
                # datos['valor'][datos['valor'] < 0] = np.nan
                datos.loc[datos['valor'] < 0, 'valor'] = np.nan
                datos=datos.dropna()
            if var.resolucion:
                datos['valor'] = datos['valor'] * float(var.resolucion)

        datos['estacion'] = estacion.est_id
        datos_variables[var.var_id_id] = datos
    return datos_variables


# guardar los vacios existentes en la información
def guardar_vacios(var_id, fecha_datos, estacion, observacion, fecha_archivo):
    variable=Variable.objects.get(var_id=var_id)
    vacio = Vacios(est_id=estacion, var_id=variable,
                   vac_fecha_ini=fecha_datos.date(),
                   vac_hora_ini=fecha_datos.time(),
                   vac_fecha_fin=fecha_archivo.date(),
                   vac_hora_fin=fecha_archivo.time(),
                   vac_observacion=observacion)
    vacio.save()


def guardar_datos_automatico(datos):
    Datos.objects.bulk_create(datos)
    Datos.objects.all().delete()
    del datos[:]


# eliminar informacion en caso de existir
def eliminar_datos(modelo, importacion, estacion):
    fecha_ini = importacion.imp_fecha_ini
    fecha_fin = importacion.imp_fecha_fin
    datos = modelo.objects.filter(fecha__gte=fecha_ini).filter(fecha__lte=fecha_fin).filter(estacion=estacion)
    if datos:
        datos.delete()


# validar si son datalogger VAISALA para restar 5 horas
def validar_datalogger(marca):
    if marca.mar_nombre == 'VAISALA':
        return True
    return False


# verificar si existen los datos
def validar_fechas(importacion):
    fecha_ini = importacion.imp_fecha_ini
    fecha_fin = importacion.imp_fecha_fin
    formato = importacion.for_id
    estacion = importacion.est_id

    clasificacion = list(Clasificacion.objects.filter(
        for_id=formato.for_id))
    result = []
    existe_vacio = False
    existe = False
    for fila in clasificacion:
        var_id = str(fila.var_id.var_id)
        est_id = str(estacion.est_id)
        modelo = get_modelo(var_id)
        fecha_datos = ultima_fecha(modelo, est_id)
        existe_vacio = existe_vacio or verificar_vacios(fecha_ini, fecha_datos)
        resumen = {
            'var_id': fila.var_id.var_id,
            'var_cod': fila.var_id.var_codigo,
            'var_nombre': fila.var_id.var_nombre,
            'ultima_fecha': fecha_datos,
            'existe': consulta_fecha(fecha_ini, fecha_fin, est_id, modelo),
            'vacio': verificar_vacios(fecha_ini, fecha_datos)
        }
        result.append(resumen)
        if fila.var_id.var_id == 11:
            resumen_caudal ={
                'var_id': 10,
                'var_cod': 'CAU',
                'var_nombre': 'Caudal',
                'ultima_fecha': ultima_fecha(modelo, est_id),
                'existe': consulta_fecha(fecha_ini, fecha_fin, est_id, modelo),
                'vacio': verificar_vacios(fecha_ini, fecha_datos)
            }
            result.append(resumen_caudal)
    # print(existe_vacio)
    return result, existe_vacio


# verficar vacios
def verificar_vacios(fecha_archivo, fecha_datos):
    estado = False
    # print(fecha_archivo,fecha_datos)
    if fecha_datos:
        intervalo = timedelta(hours=1)
        fecha_datos += intervalo
        if fecha_datos >= fecha_archivo:
            estado = False
        else:
            estado = True
    return estado


# Consultar la ultima fecha de los datos
def ultima_fecha(modelo, estacion):
    # año base de la información
    consulta = list(modelo.objects.filter(estacion=estacion).order_by('-fecha')[:1])
    if len(consulta) > 0:

        informacion = consulta[0].fecha

    if len(consulta) <= 0:
        informacion = False
    return informacion


#Consultar periodo de tiempo del archivo
def consulta_fecha(fec_ini, fec_fin, est_id, modelo):
    consulta = modelo.objects.filter(estacion=est_id).filter(fecha__gte=fec_ini).filter(fecha__lte=fec_fin)
    if consulta.exists():
        return True
    return False


def numero_punto_decimal(val_str):
    if isinstance(val_str, Number):
        return float(val_str)
    try:
        val_str = val_str.replace(",", "")
        val_num = float(val_str)
    except:
        val_num = None
    return val_num


def numero_coma_decimal(val_str):
    if isinstance(val_str, Number):
        return float(val_str)
    try:
        val_str = val_str.replace(".", "")
        val_str = val_str.replace(",", ".")
        val_num = float(val_str)
    except:
        val_num = None
    return val_num


def get_modelo(var_id):
    variable = Variable.objects.get(var_id=var_id)
    modelo = globals()[variable.var_modelo]
    return modelo
