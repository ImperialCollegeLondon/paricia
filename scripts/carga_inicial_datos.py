################################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos (iMHEA)
# basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#         Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS), Ecuador.
#         Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones creadoras,
#              ya sea en uso total o parcial del código.

import pandas as pd
import numpy
from django.apps import apps
from math import isnan
from django.db import connection


def cambiar_nan_a_None__in_dict(dict):
    res = {}
    for key, item in dict.items():
        if type(item) is str:
            if item == 'nan':
                res[key] = None
                continue

        if type(item) is float:
            if isnan(item):
                res[key] = None
                continue

        if type(item) is numpy.float64:
            if numpy.isnan(item):
                res[key] = None
                continue
        res[key] = item
    return res


def remover_nan__in_dict(dict):
    res = {}
    for key, item in dict.items():
        if type(item) is str:
            if item == 'nan':
                continue

        if type(item) is float:
            if isnan(item):
                continue

        if type(item) is numpy.float64:
            if numpy.isnan(item):
                continue
        res[key] = item
    return res


def cambiar_nan_a_None__in_list_of_dict(list):
    res = []
    for row in list:
        new_row = cambiar_nan_a_None__in_dict(row)
        res.append(new_row)
    return res

#######################################################################################################################
### Actualizar las secuencias de las llaves primarias

tempsql_seq_key = """
WITH 
col_pk AS (
	SELECT c.column_name AS colname
	FROM information_schema.table_constraints tc 
	JOIN information_schema.constraint_column_usage AS ccu USING (constraint_schema, constraint_name) 
	JOIN information_schema.columns AS c ON c.table_schema = tc.constraint_schema
	  AND tc.table_name = c.table_name AND ccu.column_name = c.column_name
	WHERE constraint_type = 'PRIMARY KEY' and tc.table_name = 'app_model'
),
seq_name AS (
	SELECT c.relname as seqname 
	FROM pg_class c WHERE c.relkind = 'S' and c.relname LIKE 'app_model\_%'
)
SELECT (SELECT colname FROM col_pk),  (SELECT seqname FROM seq_name);
"""

tempsql_update_seq = "SELECT setval('app_model_idcol_seq', COALESCE((SELECT MAX(idcol)+1 FROM app_model), 1), false);"


def actualizar_secuencia_pk(tablename):
    print("Actualizando sequencia")
    print("%s" % (tablename,))
    sql_seq_key = tempsql_seq_key.replace('app_model', tablename)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_seq_key)
            resultado = cursor.fetchone()
        col_pk = resultado[0]
        seq_name = resultado[1]
    except:
        if tablename == 'auth_user':
            col_pk = 'id'
            seq_name = 'auth_user_id_seq'
        else:
            print("        Error: No se pudo obtener sequence o column name")
            return None

    if col_pk is None or seq_name is None:
        print("        Error: No se pudo obtener sequence o column name")
        return None

    sql_update_seq = tempsql_update_seq.replace('app_model_idcol_seq', seq_name)
    sql_update_seq = sql_update_seq.replace('idcol', col_pk)
    sql_update_seq = sql_update_seq.replace('app_model', tablename)

    try:
        with connection.cursor() as cursor:
            cursor.execute(sql_update_seq)
            resultado = cursor.fetchone()[0]
        if resultado > 0:
            print("    OK: SEQ = %s" % (resultado))
            return None
    except:
        print("    Error: No se actualizó secuencia")


### Cargar información a base de datos desde archivo CSV
def cargar_archivo(directory, filename):
    data = pd.read_csv(directory + '/' + filename).to_dict('records')
    tablename = filename.rsplit('.')[0]
    app_label = tablename.split('_')[0]
    model_name = tablename.split('_')[1]
    Model = apps.get_model(app_label=app_label, model_name=model_name)
    for row in data:
        new_row = remover_nan__in_dict(row)
        Model(**new_row).save()
    actualizar_secuencia_pk(tablename)


#######################################################################################################################

directory = 'scripts/datos_inicial_20210126'

list_archivos = [
    'medicion_var1medicion.csv',
]


cargar_archivo(directory, 'medicion_var1medicion.csv')





