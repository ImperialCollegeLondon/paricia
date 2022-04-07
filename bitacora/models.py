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

from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from estacion.models import Estacion
from variable.models import Variable


class Bitacora(models.Model):
    """Possibly similar to a log entry? An observation made about some variable
    at some station between some dates. Appears under "Maintenance" on frontend
    alongside sensor installations. Perhaps intended for more general notes.
    DELETE? - Unsure how useful this is.
    NEWNAME: LogEntry
    """

    bit_id = models.AutoField("Id", primary_key=True)
    var_id = models.ForeignKey(
        Variable, models.SET_NULL, blank=True, null=True, verbose_name="Variable"
    )
    est_id = models.ForeignKey(
        Estacion, models.SET_NULL, blank=True, null=True, verbose_name="Estacion"
    )
    bit_fecha_ini = models.DateField("Fecha de inicio")
    bit_fecha_fin = models.DateField("fecha de fin", blank=True, null=True)
    bit_observacion = models.CharField("Observacion", max_length=500, blank=True)

    def __str__(self):
        return str(self.bit_id)

    def get_absolute_url(self):
        return reverse("bitacora:bitacora_index")

    class Meta:
        ordering = (
            "bit_id",
            "est_id",
            "var_id",
        )
