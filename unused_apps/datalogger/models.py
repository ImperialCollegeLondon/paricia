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


class Marca(models.Model):
    """Brand of datalogger e.g. Lascar electronics.
    GENERALISE with sensor.Brand ?
    """

    mar_id = models.AutoField("Id", primary_key=True)
    mar_nombre = models.CharField("Marca", max_length=25)

    def __str__(self):
        return self.mar_nombre

    def get_absolute_url(self):
        return reverse("datalogger:marca_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("mar_id",)


class Datalogger(models.Model):
    """Datalogger is similar to sensor.Sensor - has brand, model, serial no."""

    dat_id = models.AutoField("Id", primary_key=True)
    dat_codigo = models.CharField("Código", max_length=32)
    mar_id = models.ForeignKey(
        Marca, models.SET_NULL, blank=True, null=True, verbose_name="Marca"
    )
    dat_modelo = models.CharField("Modelo", max_length=25, null=True, blank=True)
    dat_serial = models.CharField("Serial", max_length=25, null=True, blank=True)
    dat_estado = models.BooleanField("Estado (Activo)", default=True)

    def __str__(self):
        return self.dat_codigo

    def get_absolute_url(self):
        return reverse("datalogger:datalogger_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("mar_id",)
