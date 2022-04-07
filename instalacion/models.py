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

from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from datalogger.models import Datalogger
from estacion.models import Estacion


class Instalacion(models.Model):
    ins_id = models.AutoField("Id", primary_key=True)
    est_id = models.ForeignKey(
        Estacion, models.SET_NULL, blank=True, null=True, verbose_name="Estación"
    )
    dat_id = models.ForeignKey(
        Datalogger, models.SET_NULL, blank=True, null=True, verbose_name="Datalogger"
    )
    ins_fecha_ini = models.DateField("Fecha de inicio")
    ins_fecha_fin = models.DateField("fecha de fin", blank=True, null=True)
    ins_en_uso = models.BooleanField("En uso", default=True)
    ins_observacion = models.CharField("Observacion", max_length=500, blank=True)

    def __str__(self):
        return str(self.ins_id)

    def get_absolute_url(self):
        return reverse("instalacion:instalacion_index")

    class Meta:
        ordering = (
            "ins_id",
            "est_id",
            "dat_id",
        )
