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

from estacion.models import Estacion
from variable.models import Variable


class Cruce(models.Model):
    """This model associates a Variable (e.g. Precipitation) with a Station. This is used in various
    places to filter for stations based on a specific variable, and vice versa.
    NEWNAME: StationVariable
    """

    cru_id = models.AutoField("Id", primary_key=True)
    est_id = models.ForeignKey(
        Estacion, models.SET_NULL, blank=True, null=True, verbose_name="Estación"
    )
    var_id = models.ForeignKey(
        Variable, models.SET_NULL, blank=True, null=True, verbose_name="Variable"
    )

    def __str__(self):
        return str(self.cru_id)

    def get_absolute_url(self):
        return reverse("cruce:cruce_index")

    class Meta:
        ordering = (
            "cru_id",
            "est_id",
            "var_id",
        )
        unique_together = (
            "est_id",
            "var_id",
        )
