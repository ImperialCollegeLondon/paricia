########################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos
# (iMHEA)basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#           Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS),
#           Ecuador.
#           Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones
#  creadoras, ya sea en uso total o parcial del código.
########################################################################################

from __future__ import unicode_literals

from django.db import models
from django.urls import reverse


class Tipo(models.Model):
    tip_id = models.AutoField("Id", primary_key=True)
    tip_nombre = models.CharField("Tipo", max_length=25)

    def __str__(self):
        return str(self.tip_nombre)

    def get_absolute_url(self):
        return reverse("sensor:tipo_detail", kwargs={"pk": self.pk})


class Marca(models.Model):
    mar_id = models.AutoField("Id", primary_key=True)
    mar_nombre = models.CharField("Marca", max_length=25)

    def __str__(self):
        return str(self.mar_nombre)

    def get_absolute_url(self):
        return reverse("sensor:marca_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("mar_id",)


class Sensor(models.Model):
    sen_id = models.AutoField("Id", primary_key=True)
    sen_codigo = models.CharField("Codigo", max_length=32, null=True, unique=True)
    tip_id = models.ForeignKey(
        Tipo, on_delete=models.CASCADE, verbose_name="Tipo", null=True
    )
    mar_id = models.ForeignKey(
        Marca, on_delete=models.CASCADE, verbose_name="Marca", null=True
    )
    sen_modelo = models.CharField("Modelo", max_length=150, null=True, blank=True)
    sen_serial = models.CharField("Serial", max_length=20, null=True, blank=True)
    sen_estado = models.BooleanField("Estado (Activo)", default=False)

    def __str__(self):
        return str(self.sen_codigo)

    def get_absolute_url(self):
        return reverse("sensor:sensor_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = (
            "sen_codigo",
            "tip_id",
            "mar_id",
            "sen_modelo",
        )
