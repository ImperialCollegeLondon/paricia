# -*- coding: utf-8 -*-

from estacion.models import Estacion
from variable.models import Variable
from datetime import timedelta, datetime
from django.db import connection
from math import ceil
from cruce.models import Cruce
from importacion.functions import get_modelo

suma = 'sum(valor) as valor '
promedio = 'avg(valor) as valor'
max_abs = 'max(maximo) as max_abs'
max_pro = 'max(valor) as max_pro'
min_abs = 'min(minimo) as min_abs'
min_pro = 'min(valor) as min_pro'
coma = ', '
group_order = 'GROUP BY 1 ORDER BY 1'


def datos_instantaneos(estacion, variable, fecha_inicio, fecha_fin):

    modelo = get_modelo(variable.var_id)
    fecha_inicio = datetime(fecha_inicio.year, fecha_inicio.month, fecha_inicio.day, 0, 0, 0)
    fecha_fin = datetime(fecha_fin.year, fecha_fin.month, fecha_fin.day, 23, 59, 59, 999999)
    tabla = 'medicion_' + str(variable.var_modelo)
    sql = 'SELECT * FROM ' + tabla + ' WHERE estacion =' + str(estacion.est_id)
    # if fecha_inicio:
    sql = sql + ' AND fecha>=\'' + str(fecha_inicio) + '\''
    # if fecha_fin:
    sql = sql + ' AND fecha<=\'' + str(fecha_fin) + '\''
    sql = sql + ' order by fecha ASC;'
    consulta = list(modelo.objects.raw(sql))
    valor = []
    maximo = []
    minimo = []
    frecuencia = []
    for fila in consulta:
        if fila.valor is not None:
            valor.append(fila.valor)
        else:
            valor.append(None)
        if variable.var_id != 1:
            if fila.maximo is not None:
                maximo.append(fila.maximo)
            else:
                maximo.append(None)
            if fila.minimo is not None:
                minimo.append(fila.minimo)
            else:
                minimo.append(None)
        # frecuencia.append(fila.fecha)
        frecuencia.append(fila.fecha.strftime("%Y-%m-%d %H:%M:%S"))
    return valor, maximo, minimo, frecuencia


def datos_estacion(estacion, fecha_inicio, fecha_fin):
    cruce = list(Cruce.objects.filter(est_id=estacion))
    i = 0
    i_fecha = 0
    num_variables=len(cruce)
    valores = [[0 for x in range(0)] for y in range(num_variables+1)]
    for fila in cruce:
        valor, maximo, minimo, frecuencia = datos_instantaneos(estacion, fila.var_id, fecha_inicio, fecha_fin)
        # llenar la frecuencia de tiempo
        if i == 0:
            valores[i] = set_valores(frecuencia)
            valores[i].insert(0, "Fecha hora")
            i += 1
        # comprobar si hay otras frecuecnas de tiempo ej: el viento se registra cada 2 min
        elif len(frecuencia) < (len(valores[i_fecha])-1):
            valores[i] = set_valores(frecuencia)
            valores[i].insert(0, "Fecha hora")
            i_fecha = i
            valores.append([0 for x in range(0)])
            i += 1
        # agregar el valor de cada variable
        valores[i] = set_valores(valor)
        valores[i].insert(0, fila.var_id.var_nombre)
        # verificar si hay maximos
        if contar_vacios(maximo) > 0:
            i += 1
            valores.append([0 for x in range(0)])
            valores[i] = set_valores(maximo)
            valores[i].insert(0, fila.var_id.var_nombre + " Máxima")
        # verificar si hay mínimos
        if contar_vacios(minimo)>0:
            i += 1
            valores.append([0 for x in range(0)])
            valores[i] = set_valores(minimo)
            valores[i].insert(0, fila.var_id.var_nombre + " Mínima")
        i += 1
    num_fil = len(valores[0])
    matriz = [[0 for x in range(0)] for y in range(0)]
    for i in range(len(valores)):
        if len(valores[i]) == num_fil:
            matriz.append(valores[i])
    for i in range(len(valores)):
        if len(valores[i]) < num_fil:
            matriz.append(valores[i])
    return matriz


def datos_5minutos(estacion, variable, fecha_inicio, fecha_fin):
    datos = armar_consulta(estacion, variable, 1, fecha_inicio, fecha_fin)
    valor = []
    maximo_abs = []
    maximo_pro = []
    minimo_abs = []
    minimo_pro = []
    frecuencia = []
    intervalo = timedelta(minutes=5)
    fecha = datetime.combine(fecha_inicio, datetime.min.time())
    int_5minutos = ((fecha_fin - fecha_inicio).days + 1) * 288
    num_datos = len(datos)
    item = 0
    for dia in range(int_5minutos):
        if item < num_datos:
            fecha_datos = datos[item].get('fecha')
            if fecha_datos == fecha:
                valor.append(datos[item].get('valor'))
                maximo_abs.append(datos[item].get('max_abs'))
                maximo_pro.append(datos[item].get('max_pro'))
                minimo_abs.append(datos[item].get('min_abs'))
                minimo_pro.append(datos[item].get('min_pro'))
                item += 1
            else:
                valor.append(None)
                maximo_abs.append(None)
                maximo_pro.append(None)
                minimo_abs.append(None)
                minimo_pro.append(None)
            #frecuencia.append(fecha)
            frecuencia.append(fecha.strftime("%Y-%m-%d %H:%M:%S"))
            fecha += intervalo

    return valor, maximo_abs, maximo_pro, minimo_abs, minimo_pro, frecuencia


def datos_horarios(estacion, variable, fecha_inicio, fecha_fin):
    datos = armar_consulta(estacion, variable, 2, fecha_inicio, fecha_fin)
    valor = []
    maximos_abs = []
    maximos_pro = []
    minimos_abs = []
    minimos_pro = []
    frecuencia = []
    intervalo = timedelta(hours=1)
    fecha = datetime.combine(fecha_inicio, datetime.min.time())
    int_horas = ((fecha_fin - fecha_inicio).days + 1) * 24
    num_datos = len(datos)
    item = 0
    for dia in range(int_horas):
        if item < num_datos:
            fecha_datos = datos[item].get('fecha')
            if fecha_datos == fecha:
                valor.append(datos[item].get('valor'))
                maximos_abs.append(datos[item].get('max_abs'))
                maximos_pro.append(datos[item].get('max_pro'))
                minimos_abs.append(datos[item].get('min_abs'))
                minimos_pro.append(datos[item].get('min_pro'))
                item += 1
            else:
                valor.append(None)
                maximos_abs.append(None)
                maximos_pro.append(None)
                minimos_abs.append(None)
                minimos_pro.append(None)
            # frecuencia.append(fecha)
            frecuencia.append(fecha.strftime("%Y-%m-%d %H:%M:%S"))
            fecha += intervalo
    return valor, maximos_abs, maximos_pro, minimos_abs, minimos_pro, frecuencia


def datos_diarios(estacion, variable, fecha_inicio, fecha_fin):
    datos = armar_consulta(estacion, variable, 3, fecha_inicio, fecha_fin)
    valor = []
    # maximos absolutos
    maximos_abs = []
    maximos_pro = []
    minimos_abs = []
    minimos_pro = []
    frecuencia = []
    intervalo = timedelta(days=1)

    fecha = fecha_inicio
    int_dias = (fecha_fin - fecha_inicio).days + 1
    num_datos = len(datos)
    item = 0
    for dia in range(int_dias):
        if item < num_datos:
            fecha_datos = datos[item].get('fecha').date()
            if fecha_datos == fecha:

                valor.append(datos[item].get('valor'))
                maximos_abs.append(datos[item].get('max_abs'))
                maximos_pro.append(datos[item].get('max_pro'))
                minimos_abs.append(datos[item].get('min_abs'))
                minimos_pro.append(datos[item].get('min_pro'))
                item += 1
            else:
                valor.append(None)
                maximos_abs.append(None)
                maximos_pro.append(None)
                minimos_abs.append(None)
                minimos_pro.append(None)
            frecuencia.append(fecha)
            fecha += intervalo
    return valor, maximos_abs, maximos_pro, minimos_abs, minimos_pro, frecuencia


def datos_mensuales(estacion, variable, fecha_inicio, fecha_fin):
    datos = armar_consulta(estacion, variable, 4, fecha_inicio, fecha_fin)
    valor = []
    maximo_abs = []
    maximo_pro = []
    minimo_abs = []
    minimo_pro = []
    frecuencia = []
    fecha = fecha_inicio.replace(day=1)
    # intervalo = timedelta(days=30)
    dias = float((fecha_fin - fecha_inicio).days)
    meses = int(ceil(dias / 30))
    num_datos = len(datos)
    item = 0
    for mes in range(meses):
        if item < num_datos:
            fecha_datos = datos[item].get('fecha').date()
            if fecha == fecha_datos:
                valor.append(datos[item].get('valor'))
                maximo_abs.append(datos[item].get('max_abs'))
                maximo_pro.append(datos[item].get('max_pro'))
                minimo_abs.append(datos[item].get('min_abs'))
                minimo_pro.append(datos[item].get('min_pro'))
                item += 1
            else:
                valor.append(None)
                maximo_abs.append(None)
                maximo_pro.append(None)
                minimo_abs.append(None)
                minimo_pro.append(None)
            frecuencia.append(fecha)
            intervalo = dias_mes(fecha.month, fecha.year)
            fecha += timedelta(days=intervalo)

    return valor, maximo_abs, maximo_pro, minimo_abs, minimo_pro, frecuencia


def armar_consulta(estacion, variable, frecuencia, fecha_inicio, fecha_fin):

    cursor = connection.cursor()
    # datos = []
    fecha_inicio = datetime(fecha_inicio.year, fecha_inicio.month, fecha_inicio.day, 0, 0, 0)
    fecha_fin = datetime(fecha_fin.year, fecha_fin.month, fecha_fin.day, 23, 59, 59, 999999)
    fecha = ""
    if frecuencia == 1:
        fecha = 'to_timestamp(floor((extract(\'epoch\' '
        fecha += 'from fecha) / 300 )) * 300)'
        fecha += 'AT TIME ZONE \'UTC5\' as fecha, '
    elif frecuencia == 2:
        fecha = 'date_trunc(\'hour\',fecha) as fecha, '
    elif frecuencia == 3:
        fecha = 'date_trunc(\'day\',fecha) as fecha, '
    elif frecuencia == 4:
        fecha = 'date_trunc(\'month\',fecha) as fecha, '
    tabla = 'medicion_' + str(variable.var_modelo)
    filtro = 'estacion=' + str(estacion.est_id) + ' and valor !=\'NaN\'::numeric '
    if fecha_inicio:
        filtro += ' and fecha>=\'' + str(fecha_inicio) + '\''
    if fecha_fin:
        filtro += ' and fecha<=\'' + str(fecha_fin) + '\' '

    if variable.var_id == 1:
        sql = 'SELECT ' + fecha + suma
        sql += ' FROM ' + tabla + ' WHERE '
        sql += filtro + group_order
    else:
        sql = 'SELECT ' + fecha
        sql += promedio + coma + max_abs + coma + max_pro + coma + min_abs + coma + min_pro
        sql += ' FROM ' + tabla + ' WHERE '
        sql += filtro + group_order
    cursor.execute(sql)
    print(sql)
    datos = dictfetchall(cursor)
    cursor.close()
    return datos


def dias_mes(month, year):
    dias = 30
    if month <= 7:
        if month % 2 == 0 and month != 2:
            dias = 30
        elif month % 2 == 0 and month == 2:
            if year % 4 == 0:
                dias = 29
            else:
                dias = 28
        else:
            dias = 31
    else:
        if month % 2 == 0:
            dias = 31
        else:
            dias = 30
    return dias


def titulo_frecuencia(frecuencia):
    nombre = []
    if frecuencia == '0':
        nombre = 'Instantanea'
    if frecuencia == '1':
        nombre = '5 Minutos'
    elif frecuencia == '2':
        nombre = 'Horaria'
    elif frecuencia == '3':
        nombre = 'Diaria'
    elif frecuencia == '4':
        nombre = 'Mensual'
    return nombre


def dictfetchall(cursor):
    # Return all rows from a cursor as a dict
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def datos_horarios_json(est_id, var_id, fec_ini, fec_fin):
    fecha_ini = datetime.strptime(fec_ini, '%Y-%m-%d %H:%M:%S')
    fecha_fin = datetime.strptime(fec_fin, '%Y-%m-%d %H:%M:%S')
    datos = []
    estacion = Estacion.objects.get(est_id=est_id)
    variable = Variable.objects.get(var_id=var_id)
    val, max_abs, max_pro, min_abs, min_pro, time = \
        datos_horarios(estacion, variable, fecha_ini, fecha_fin)
    if len(val) > 0:
        for item_val, item_max_abs, item_max_pro, item_min_abs, item_min_pro, item_time \
                in zip(val, max_abs, max_pro, min_abs, min_pro, time):
            if fecha_ini <= datetime.strptime(item_time, '%Y-%m-%d %H:%M:%S') <= fecha_fin:
                dato = {
                    'fecha': item_time,
                    'valor': item_val,
                    'maximo_absoluto': item_max_abs,
                    'minimo_absolulo': item_min_abs,
                    'maximo_promedio': item_max_pro,
                    'minimo_promedio': item_min_pro,
                }
                datos.append(dato)
    else:
        datos = {
            'mensaje': 'no hay datos'
        }
    return datos


def contar_vacios(valores):
    num_vacios = 0
    for item in valores:
        if item is not None:
            num_vacios += 1
    return num_vacios


def set_valores(valores):
    datos = []
    for item in valores:
        if item is not None:
            datos.append(item)
        else:
            datos.append('')
    return datos
