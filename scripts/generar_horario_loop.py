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
Computes hourly data from 5,1,30 minute data. It's intended to be called once a day in case the regular flow for
computing hourly data has failed.
(regular flow is a background thread that is launched after validation process. /
See validacion/views.py:generar_reportes_1variable() )

It performs the POSTGRESQL function `generar_horario_varN` in a loop until there's no more data
marked as FALSE in `usado_para_horario` (used for hourly) flag.

This script is called by a crontab activity once a day.

The function `generar_horario_varN` is defined in the templates `scripts/plpgsql/generar_horario_xxxx.sql`
and its installed once at installation process. See script: `scripts/instalar_funciones_postgres.py`
"""


from django.db import connection

from variable.models import Variable


def run():
    cursor = connection.cursor()
    variables = Variable.objects.filter(reporte_automatico=True)
    for variable in variables:
        sql = "SELECT * FROM generar_horario_var" + str(variable.var_id) + "();"
        res = True
        while res:
            cursor.execute(sql)
            res = cursor.fetchone()[0]
