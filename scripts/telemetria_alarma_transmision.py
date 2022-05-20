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


"""Check the state of automatic transmitted stations

This script is called every hour and check the last time each automatic station is transmitted
In case a station has not been transmitted for the last hour then the script set a flag to 'YELLOW ALERT'
In case a station has not been transmitted for the last 24 hours then the script set a flag to 'RED ALERT'
    and an automatic email is sent to a mail list.

The threshold values are set via the web interface.
The mail list is also configured via the web interface.

See:
    telemetria/functions.py:  consulta_alarma_transmision()

"""


import datetime
import itertools

import pytz
from django.core.mail import send_mail
from django.db import connection

from telemetria.models import (
    AlarmaEmail,
    AlarmaEstado,
    AlarmaTipoEstado,
    ConfigVisualizar,
    TeleVariables,
)

try:
    lim_inf_horas = TeleVariables.objects.get(nombre="ALAR_TRAN_LIMI_INFE").valor
    lim_sup_horas = TeleVariables.objects.get(nombre="ALAR_TRAN_LIMI_SUPE").valor
    estado = {}
    for e in AlarmaTipoEstado.objects.all():
        estado[e.nombre] = e.id
except:
    quit()


# fecha_actual = datetime.datetime.now(pytz.utc)
# fecha_actual = fecha_actual.replace(tzinfo=None)
fecha_actual = datetime.datetime.now()

configvisualizar = ConfigVisualizar.objects.all().order_by("estacion_id")

fallos = []
estacion_verificada = None
for est_var in configvisualizar:
    ## Si es caudal no se tomará en cuenta porque caudal es una variable derivada usando curva de descarga y nivel
    ## Hubo problema en alarma de transmisión porque Si se recibía NIVEL pero no se calculaba CAUDAL por que no hubo
    ## curva de descarga aún y por lo tanto daba un falso positivo.
    if est_var.variable_id == 10:
        continue

    if est_var.estacion_id == estacion_verificada:
        continue
    estacion_verificada = est_var.estacion_id

    sql = """SELECT fecha FROM medicion_var|var_id|medicion 
    WHERE estacion_id = %s AND fecha <= %s
    ORDER BY fecha DESC LIMIT 1;
    """
    sql = sql.replace("|var_id|", str(est_var.variable_id))
    with connection.cursor() as cursor:
        cursor.execute(sql, (est_var.estacion_id, fecha_actual))
        res = cursor.fetchone()

    try:
        fecha_dato = res[0]
        diff = fecha_actual - fecha_dato
        diff_horas = diff.days * 24 + diff.seconds / 3600
    except:
        AlarmaEstado.objects.update_or_create(
            estacion_id=est_var.estacion_id,
            fecha=fecha_actual,
            defaults={"estado_id": estado["FALLO"]},
        )
        continue

    if diff_horas <= lim_inf_horas:
        estado_actual = "NORMAL"
    elif diff_horas <= lim_sup_horas:
        estado_actual = "EXPECTANTE"
    else:
        estado_actual = "FALLO"

    try:
        alarmaestado_anterior = (
            AlarmaEstado.objects.filter(estacion_id=est_var.estacion_id)
            .order_by("-fecha")
            .first()
        )
        estado_anterior = alarmaestado_anterior.estado.nombre
    except:
        estado_anterior = ""

    if estado_actual == estado_anterior:
        continue

    AlarmaEstado.objects.update_or_create(
        estacion_id=est_var.estacion_id,
        fecha=fecha_actual,
        defaults={"estado_id": estado[estado_actual]},
    )

    if estado_actual == "FALLO":
        # enviar correo
        reporte = {
            "estacion": est_var.estacion.est_codigo,
            "ultimo_dato": fecha_dato,
        }
        fallos.append(reporte)

###############################
# Aquí se envían los correos de los fallos
if not fallos:
    quit()

correos = AlarmaEmail.objects.all().values_list("email")
correos_destino = list(itertools.chain(*correos))
if not correos_destino:
    quit()

titulo = "iMHEA: Alerta de transmisión."
mensaje = (
    "Se reporta un fallo en la transmisión de una o más estaciones. "
    + "Las estaciones en la lista a continuación no han transmitido en las últimas "
    + str(round(lim_sup_horas, 1))
    + " horas:\n\n"
)
for e in fallos:
    mensaje = (
        mensaje
        + e["estacion"]
        + ". Último dato recibido: "
        + e["ultimo_dato"].strftime("%Y-%d-%m %H:%M:%S")
        + "\n"
    )
mensaje = (
    mensaje
    + "\n\nEste correo fue generado a las "
    + fecha_actual.strftime("%Y-%d-%m %H:%M:%S")
)
email_origen = "imheasis@condesan.org"
send_mail(
    titulo,
    mensaje,
    email_origen,
    correos_destino,
    fail_silently=False,
)
