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
from sensor.models import Sensor


class Unidad(models.Model):
    uni_id = models.AutoField("Id", primary_key=True)
    uni_nombre = models.CharField("Nombre", max_length=50)
    uni_sigla = models.CharField("Sigla", max_length=10)

    def __str__(self):
        return str(self.uni_sigla)

    def get_absolute_url(self):
        return reverse("variable:unidad_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["uni_id"]


class Variable(models.Model):
    var_id = models.AutoField("Id", primary_key=True)
    var_codigo = models.CharField("Codigo", max_length=7)
    var_nombre = models.CharField("Nombre", max_length=50)
    # var_modelo = models.CharField("Modelo",max_length=50, blank=True, null=True)
    uni_id = models.ForeignKey(
        Unidad, models.SET_NULL, blank=True, null=True, verbose_name="Unidad"
    )
    var_maximo = models.DecimalField("Maximo", max_digits=7, decimal_places=2)
    var_minimo = models.DecimalField("Minimo", max_digits=7, decimal_places=2)
    var_sos = models.DecimalField(
        "Incremento sospechoso", max_digits=7, decimal_places=2, null=True, blank=True
    )
    var_err = models.DecimalField(
        "Incremento error", max_digits=7, decimal_places=2, null=True, blank=True
    )
    var_min = models.DecimalField(
        "Sigmas (outliers)", max_digits=7, decimal_places=2, null=True, blank=True
    )
    var_estado = models.BooleanField("Estado", default=True)
    es_acumulada = models.BooleanField(
        "Acumulada (check)/ Promediada", default=True
    )  # True: ACUMULADA, False: PROMEDIADA
    reporte_automatico = models.BooleanField("Reporte Automático", default=True)
    vacios = models.DecimalField(
        "Vacíos (%)", max_digits=4, decimal_places=1, null=True
    )

    def __str__(self):
        return str(self.var_nombre)

    def get_absolute_url(self):
        return reverse("variable:variable_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["var_id"]


class Control(models.Model):
    con_id = models.AutoField("Id", primary_key=True)
    var_id = models.ForeignKey(
        Variable, models.SET_NULL, blank=True, null=True, verbose_name="Variable"
    )
    est_id = models.ForeignKey(
        Estacion, models.SET_NULL, blank=True, null=True, verbose_name="Estación"
    )
    sen_id = models.ForeignKey(
        Sensor, models.SET_NULL, blank=True, null=True, verbose_name="Sensor"
    )
    con_fecha_ini = models.DateField("Fecha inicio")
    con_fecha_fin = models.DateField("Fecha fin", blank=True, null=True)
    con_estado = models.BooleanField("Activo", default=True)

    def get_absolute_url(self):
        return reverse("variable:control_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["est_id"]


class CurvaDescarga(models.Model):
    estacion = models.ForeignKey(
        Estacion,
        on_delete=models.CASCADE,
        verbose_name="Estacion",
        related_name="var_curvadescarga_estacion_id",
    )
    funcion = models.CharField("Función", max_length=200)
    fecha = models.DateField("Fecha")
