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


"""
Computes monthly data from daily data. It's intended to be called once a day in case the regular flow for
computing monthly data has failed.
 (regular flow is a background thread that is launched after validation process. /
 See validacion/views.py:generar_reportes_1variable() )

It performs the POSTGRESQL function `generar_mensual_var1` in a loop until there's no more data
marked as FALSE in `usado_para_mensual` (used for monthly) flag.

This script is called by a crontab activity once a day.

The function `generar_mensual_var1` is defined in the template `scripts/plpgsql/generar_mensual_var1.sql`
and it is installed once at installation process. See script: `scripts/instalar_funciones_postgres2.py`
"""


from django.db import connection

from variable.models import Variable


def run():
    cursor = connection.cursor()
    variables = Variable.objects.filter(reporte_automatico=True)
    for variable in variables:
        sql = "SELECT * FROM generar_mensual_var" + str(variable.var_id) + "();"
        res = True
        while res:
            cursor.execute(sql)
            res = cursor.fetchone()[0]
