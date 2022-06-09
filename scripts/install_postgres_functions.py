"""Installation script for POSTGRES functions. A much shorter version of the original
file unused_scripts/instalar_funciones_postgres.py. More functions can be moved from
thre to here as they are needed.
"""

from django.db import connection


def functions_for_importing():
    """
    - Installs POSTGRES data type needed for 'importing' app
        scripts/plpgsql/insertar_validacion_requisitos.sql:
    """
    print("Functions for importing app")
    file = open("scripts/plpgsql/insertar_validacion_requisitos.sql", "r")
    sql = file.read()
    with connection.cursor() as cursor:
        cursor.execute(sql)


def run():
    functions_for_importing()
