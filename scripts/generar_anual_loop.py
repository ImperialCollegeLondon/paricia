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

from django.db import connection
from variable.models import Variable

def run():
    cursor = connection.cursor()
    variables = Variable.objects.filter(reporte_automatico=True)
    # for variable in variables:
    #     #generar_anual_precipitacion
    #     sql = "SELECT * FROM generar_anual_" + str(variable.var_modelo).lower() + "();"
    #     res = True
    #     while res:
    #         cursor.execute(sql)
    #         res = cursor.fetchone()[0]
    sql = sql = "SELECT * FROM generar_anual_var1();"
    res = True
    while res:
        cursor.execute(sql)
        res = cursor.fetchone()[0]
    print("cerrando la coneccion")
    cursor.close()