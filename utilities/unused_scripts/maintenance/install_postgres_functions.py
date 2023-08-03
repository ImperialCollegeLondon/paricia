"""
Installation script for POSTGRES functions. A much shorter version of the original
file unused_scripts/instalar_funciones_postgres.py. More functions can be moved from
there to here as they are needed.

NOTE: This script is not used anymore.
"""

from logging import getLogger
from pathlib import Path

from django.db import connection


def functions_for_importing():
    """
    - Installs POSTGRES data type needed for 'importing' app
        utilities/plpgsql/insertar_validacion_requisitos.sql:
    """
    getLogger().info("Functions for importing app")

    with Path("utilities/plpgsql/insertar_validacion_requisitos.sql").open("r") as file:
        sql = file.read()
    with connection.cursor() as cursor:
        cursor.execute(sql)


def run():
    functions_for_importing()
