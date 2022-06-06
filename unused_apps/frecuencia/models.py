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

from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

from estacion.models import Estacion
from variable.models import Variable


class Frecuencia(models.Model):
    """A frequency (in minutes) of a Variable at a Station, between two dates.
    NEWNAME: Frequency
    """

    fre_id = models.AutoField("Id", primary_key=True)
    est_id = models.ForeignKey(
        Estacion, on_delete=models.SET_NULL, verbose_name="Estación", null=True
    )
    var_id = models.ForeignKey(
        Variable, on_delete=models.SET_NULL, verbose_name="Variable", null=True
    )
    fre_valor = models.IntegerField(
        "Frecuencia (minutos)",
        validators=[MaxValueValidator(1500), MinValueValidator(0)],
    )
    fre_fecha_ini = models.DateTimeField("Fecha inicio")
    fre_fecha_fin = models.DateTimeField("Fecha fin", blank=True, null=True)

    class Meta:
        indexes = [
            models.Index(fields=["est_id", "var_id", "fre_fecha_ini"]),
            models.Index(fields=["var_id", "est_id", "fre_fecha_ini"]),
            models.Index(fields=["fre_fecha_ini", "est_id", "var_id"]),
        ]

    def get_absolute_url(self):
        return reverse("frecuencia:frecuencia_detail", kwargs={"pk": self.pk})


##


class TipoFrecuencia(models.Model):
    """Type of Frequency e.g. monthly, daily. Used to filter reports.
    HELPWANTED: Not clear how these are actually related to the data. --> DIEGO: I don't
    see this being used in any meaningful way. Maybe is a feature not fully implemented
    or some sort of placeholder? Maybe a question for Pablo.
    NEWNAME: FrequencyType
    """

    nombre = models.CharField(max_length=25, verbose_name="Frecuencia")

    class Meta:
        indexes = [
            models.Index(fields=["nombre"]),
        ]

    def __str__(self):
        return str(self.nombre)


class UsuarioTipoFrecuencia(models.Model):
    """Similar to TipoFrecuencia but with a specific user."""

    usuario = models.ForeignKey(User, on_delete=models.PROTECT)
    tipofrecuencia = models.ForeignKey(
        TipoFrecuencia, on_delete=models.PROTECT, verbose_name="Frecuencia"
    )

    class Meta:
        unique_together = ["usuario", "tipofrecuencia"]

    def __str__(self):
        return str(self.usuario.username + " - " + self.tipofrecuencia.nombre)
