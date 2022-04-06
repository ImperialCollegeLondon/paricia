# -*- coding: utf-8 -*-

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

from excel_response import ExcelResponse
from .models import Datalogger


def excel_datalogger():
    """Returns an excel spreadsheet given a QuerySet of DataLoggers."""
    cabecera = [
        ["Código", "Marca", "Modelo", "Serial"],
    ]
    cuerpo = []
    objetos = Datalogger.objects.all()
    for objeto in objetos:
        fila = []
        fila.append(objeto.dat_codigo)
        fila.append(objeto.mar_id.mar_nombre if objeto.mar_id is not None else None)
        fila.append(objeto.dat_modelo)
        fila.append(objeto.dat_serial)

        cuerpo.append(fila)
    response = ExcelResponse(cabecera + cuerpo, "Dataloggeres_iMHEA")
    return response
