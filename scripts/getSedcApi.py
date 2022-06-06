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

"""Get external data using a web service request
This tool was created to meet specific needs for an institution who wanted to extract data for an external server.

This script was executed every hour via crontab.
"""


import json
from builtins import print

import requests
from django.db import connection
from estacion.models import Estacion, Tipo
from validacion.models import Var1Validado

mainurl = "http://localhost:8002/"

##en el el SEDC http://localhost:8002/api/?var=precipitacion&estacion_id=1&fecha=2018-01
def getEstaciones():
    print("Lamando a la funcion estaciones")
    newurl = mainurl + "estaciones/"
    r = requests.get(url=newurl)
    if r.status_code == 200:
        return json.loads(r.text)


def loadEstaciones(dataJson):
    print(dataJson[0])
    dict = dataJson[0]
    for key in dict:
        print(type(key), key, type(dict[key]), dict[key])
    # for key in dataJson:
    #    print(key['est_codigo'])


def GuardaEstaciones(estDict):
    # {'est_id': 1, 'est_codigo': 'C01', 'est_nombre': 'Maucatambo', 'tipo': 2, 'provincia': 19, 'sitiocuenca': 23,
    #  'est_estado': True, 'est_longitud': '517419.37', 'est_latitud': '9924715.44', 'est_altura': 3840,
    #  'est_ficha': None}
    # nesC = ""
    # Estacion.objects.create()
    pass


def getvalidado(est_id, fecha):
    newurl = (
        mainurl
        + "inst/?var=precipitacion&estacion_id="
        + str(est_id)
        + "&fecha="
        + fecha
    )
    print(newurl)
    r = requests.get(newurl)
    print(r.status_code)
    if r.status_code == 200:
        jdat = json.loads(r.text)

    return jdat


def insertValidados(jdat, est_id):
    # ?var=precipitacion&estacion_id=1&fecha=2019-06-04
    #  ?var = variable & estacion_id = codigo_estacion & fecha = año-mes-dia
    # sql = "SELECT * FROM generar_horario_" + variable + "();"

    # cursor = connection.cursor()
    # sql = "select * from estacion_estacion where est_codigo = 'M5021';"
    # cursor.execute(sql)
    # row = cursor.fetchone()
    # print(row[0], row[1], row[2])
    cursor = connection.cursor()
    # estacion_id , fecha, valor
    # INSERT INTO public.validacion_precipitacion(estacion_id, fecha, valor, usado_para_horario, validacion) VALUES (1, '2019-06-01 00:00:06',8.1,false, 0);
    if len(jdat) > 0:
        for i in jdat:
            est = i["estacion_id"]
            fec = i["fecha"].replace("T", " ")
            val = i["valor"]
            # insertSql = "INSERT INTO public.validacion_precipitacion(estacion_id, fecha, valor, usado_para_horario, validacion) VALUES ("++""
            Var1Validado.objects.create(
                estacion_id=est_id,
                fecha=fec,
                valor=val,
                usado_para_horario=False,
                validacion=0,
            )
            # precipitacion.seve()

            print("insertando " + fec)
        sql = "SELECT * FROM generar_horario_precipitacion();"
        # cursor.execute(sql)
        # print("Datos horarios generados "+cursor.fetchone()[0])

        sql = "SELECT * FROM generar_diario_precipitacion();"
        # cursor.execute(sql)
        # print("Datos diarios generados "+cursor.fetchone()[0])

        sql = "SELECT * FROM generar_mensual_precipitacion();"
        # cursor.execute(sql)
        # print("Datos mensuales generados "+cursor.fetchone()[0])
    else:
        print("No hay nada para procesar....")


# --args Testing
def run(*args):
    print(args)
    est_codigo = args[0]
    estLoc = Estacion.objects.filter(est_codigo__exact=est_codigo).values(
        "est_id", "est_nombre"
    )[0]
    est_id = estLoc["est_id"]
    fecha = args[1]
    data = getvalidado(1, fecha)
    insertValidados(data, est_id)


#########Ejecutar con    python manage.py runscript getSedcApi --script-args M5021 2019-06-01
