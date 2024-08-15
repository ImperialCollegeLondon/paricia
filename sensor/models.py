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


from django.db import models
from django.urls import reverse

from management.models import PermissionsBase


class SensorType(PermissionsBase):
    """Type of sensor, eg. pluviometric, wind sensor, etc."""

    type_id = models.AutoField("Id", primary_key=True)
    name = models.CharField("Sensor type", max_length=25)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("sensor:type_detail", kwargs={"pk": self.pk})


class SensorBrand(PermissionsBase):
    """Brand of the sensor, eg. Davis, Texas Electronics, etc."""

    brand_id = models.AutoField("Id", primary_key=True)
    name = models.CharField("Brand name", max_length=25)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("sensor:brand_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("brand_id",)


class Sensor(PermissionsBase):
    """Specific sensor details"""

    sensor_id = models.AutoField("Id", primary_key=True)
    code = models.CharField("Code", max_length=32, null=True, unique=True)
    sensor_type = models.ForeignKey(
        SensorType, on_delete=models.SET_NULL, verbose_name="Sensor type", null=True
    )
    sensor_brand = models.ForeignKey(
        SensorBrand, on_delete=models.SET_NULL, verbose_name="Sensor brand", null=True
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
