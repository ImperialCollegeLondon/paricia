from telemetria.models import ConfigVisualizar, AlarmaEstado, TeleVariables, AlarmaTipoEstado, AlarmaEmail
from estacion.models import Estacion
import datetime, pytz
from django.db import connection
from django.core.mail import send_mail
import itertools

import time
import daemon


def run(*args):
    with daemon.DaemonContext():
        activar_revision()


def activar_revision():
    while True:
        lim_inf_horas, lim_sup_horas = consultar_parametros()
        fallos = revisar_transmision(lim_inf_horas, lim_sup_horas)
        enviar_alarma(fallos, lim_sup_horas)
        time.sleep(6000)


def consultar_parametros():
    try:
        lim_inf_horas = TeleVariables.objects.get(nombre='ALAR_TRAN_LIMI_INFE').valor
        lim_sup_horas = TeleVariables.objects.get(nombre='ALAR_TRAN_LIMI_SUPE').valor

    except:
        lim_inf_horas = 2
        lim_sup_horas = 24
        registrar_log("Se debe configurar los parametros: ALAR_TRAN_LIMI_INFE y ALAR_TRAN_LIMI_SUPE")
        pass
    return lim_inf_horas, lim_sup_horas


def enviar_alarma(fallos, lim_sup_horas):
    ###############################
    # Aquí se envían los correos de los fallos
    fecha_actual = datetime.datetime.now()
    if len(fallos) > 0:
        correos = AlarmaEmail.objects.all().values_list('email')
        correos_destino = list(itertools.chain(*correos))
        if correos_destino:

            titulo = 'SEDC: Alerta de transmisión.'
            mensaje = "Se reporta un fallo en la transmisión de una o más estaciones. " + \
                      "Las estaciones en la lista a continuación no han transmitido en las últimas " + \
                      str(round(lim_sup_horas, 1)) + " horas:\n\n"
            for e in fallos:
                mensaje = mensaje + e['estacion'] + '. Último dato recibido: ' + e['ultimo_dato'].strftime(
                    "%Y-%d-%m %H:%M:%S") + '\n'
            mensaje = mensaje + "\n\nEste correo fue generado a las " + fecha_actual.strftime("%Y-%d-%m %H:%M:%S")
            email_origen = 'paul.chicaiza@fonag.org.ec'
            send_mail(
                titulo,
                mensaje,
                email_origen,
                correos_destino,
                fail_silently=False,
            )
        else:
            registrar_log("No existen correos para reportar problemas en la transmision")
    else:
        registrar_log("No existe fallo en la transmision")


def revisar_transmision(lim_inf_horas, lim_sup_horas):
    # lim_inf_horas = TeleVariables.objects.get(nombre='ALAR_TRAN_LIMI_INFE').valor
    # lim_sup_horas = TeleVariables.objects.get(nombre='ALAR_TRAN_LIMI_SUPE').valor
    estado = {}
    for e in AlarmaTipoEstado.objects.all():
        estado[e.nombre] = e.id

    fecha_actual = datetime.datetime.now()
    configvisualizar = ConfigVisualizar.objects.all().order_by('estacion_id')

    fallos = []
    estacion_verificada = None
    for fila_cv in configvisualizar:
        ## Si es caudal no se tomará en cuenta porque caudal es una variable derivada usando curva de descarga y nivel
        ## Hubo problema en alarma de transmisión porque Si se recibía NIVEL pero no se calculaba CAUDAL por que no hubo
        ## curva de descarga aún y por lo tanto daba un falso positivo.
        if fila_cv.variable_id == 10:
            continue
        if fila_cv.estacion_id == estacion_verificada:
            continue
        estacion_verificada = fila_cv.estacion_id

        sql = """SELECT fecha FROM medicion_|var_id| 
            WHERE estacion_id = %s AND fecha <= %s
            ORDER BY fecha DESC LIMIT 1;
            """
        sql = sql.replace('|var_id|', str(fila_cv.variable.var_modelo))
        with connection.cursor() as cursor:
            cursor.execute(sql, (fila_cv.estacion_id, fecha_actual))
            res = cursor.fetchone()

        try:
            fecha_dato = res[0]
            diff = fecha_actual - fecha_dato
            diff_horas = diff.days * 24 + diff.seconds / 3600
        except e:
            AlarmaEstado.objects.update_or_create(
                estacion_id=fila_cv.estacion_id, fecha=fecha_actual, fecha_dato=None,
                defaults={"estado_id": estado['FALLO']}
            )
            continue

        if diff_horas <= lim_inf_horas:
            estado_actual = 'NORMAL'
        elif diff_horas <= lim_sup_horas:
            estado_actual = 'EXPECTANTE'
        else:
            estado_actual = 'FALLO'

        try:
            alarmaestado_anterior = AlarmaEstado.objects.filter(estacion_id=fila_cv.estacion_id).order_by(
                '-fecha').first()
            estado_anterior = alarmaestado_anterior.estado.nombre
        except:
            estado_anterior = ''
        # Saltar si el estado anterior no cambia
        if estado_actual == estado_anterior:
            AlarmaEstado.objects.update_or_create(
                estacion_id=fila_cv.estacion_id, fecha=fecha_actual, fecha_dato=fecha_dato,
                defaults={"estado_id": estado[estado_anterior]}
            )
            continue

        AlarmaEstado.objects.update_or_create(
            estacion_id=fila_cv.estacion_id, fecha=fecha_actual, fecha_dato=fecha_dato,
            defaults={"estado_id": estado[estado_actual]}
        )

        if estado_actual == 'FALLO':
            # enviar correo
            reporte = {
                'estacion': fila_cv.estacion.est_codigo + ' - ' + fila_cv.estacion.est_nombre,
                'ultimo_dato': fecha_dato,
            }
            fallos.append(reporte)
        return fallos


def registrar_log(mensaje):
    registro = open('/tmp/transmision.txt', 'a')
    registro.write(time.ctime() + ': ' + mensaje + '\n')
    registro.close()
