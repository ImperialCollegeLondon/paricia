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

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()


class SensorType(models.Model):
    """
    Type of sensor, eg. pluviometric, wind sensor, etc.
    """

    type_id = models.AutoField("Id", primary_key=True)
    name = models.CharField("Sensor type", max_length=25)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("sensor:type_detail", kwargs={"pk": self.pk})


class SensorBrand(models.Model):
    """
    Brand of the sensor, eg. Davis, Texas Electronics, etc.
    """

    brand_id = models.AutoField("Id", primary_key=True)
    name = models.CharField("Brand name", max_length=25)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("sensor:brand_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("brand_id",)


class Sensor(models.Model):
    """
    Specific sensor details
    """

    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    PERMISSIONS_LEVELS = [
        ("public", "Public"),
        ("internal", "Internal"),
        ("private", "Private"),
    ]

    permissions_level = models.CharField(
        max_length=8, choices=PERMISSIONS_LEVELS, default="private"
    )

    sensor_id = models.AutoField("Id", primary_key=True)
    code = models.CharField("Code", max_length=32, null=True, unique=True)
    sensor_type = models.ForeignKey(
        SensorType, on_delete=models.CASCADE, verbose_name="Sensor type", null=True
    )
    sensor_brand = models.ForeignKey(
        SensorBrand, on_delete=models.CASCADE, verbose_name="Sensor brand", null=True
    )
    model = models.CharField("Model", max_length=150, null=True, blank=True)
    serial = models.CharField("Serial number", max_length=20, null=True, blank=True)
    status = models.BooleanField("Status (active)", default=False)

    def __str__(self):
        return str(self.code)

    def get_absolute_url(self):
        return reverse("sensor:sensor_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = (
            "code",
            "sensor_type",
            "sensor_brand",
            "model",
        )
