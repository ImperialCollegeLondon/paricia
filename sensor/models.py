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
    """Type of sensor, eg. pluviometric, wind sensor, etc.

    Attributes:
        sensor_type_id: int, primary key, sensor type id.
        name: str, sensor type name.
    """

    type_id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    name = models.CharField("Sensor type", max_length=25, help_text="Sensor type name.")

    def __str__(self) -> str:
        """Return the sensor type name."""
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Return the absolute url of the sensor type."""
        return reverse("sensor:type_detail", kwargs={"pk": self.pk})


class SensorBrand(PermissionsBase):
    """Brand of the sensor, eg. Davis, Texas Electronics, etc.

    Attributes:
        brand_id: int, primary key, sensor brand id.
        name: str, sensor brand name.
    """

    brand_id = models.AutoField("Id", primary_key=True, help_text="Primary key")
    name = models.CharField("Brand name", max_length=25, help_text="Name of the brand.")

    def __str__(self) -> str:
        """Return the brand name."""
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Return the absolute url of the sensor brand."""
        return reverse("sensor:brand_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("brand_id",)


class Sensor(PermissionsBase):
    """Specific sensor details.

    Attributes:
        sensor_id (int): Primary key, sensor id.
        code: (str) sensor code.
        sensor_type (SensorType): sensor type.
        sensor_brand (SensorBrand): sensor brand.
        model (str): specific model of the sensor.
        serial (str): serial number of the sensor.
        status (bool): sensor status.
    """

    sensor_id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    code = models.CharField(
        "Code", max_length=32, unique=True, help_text="Sensor code."
    )
    sensor_type = models.ForeignKey(
        SensorType,
        on_delete=models.PROTECT,
        verbose_name="Sensor type",
        help_text="Sensor type.",
    )
    sensor_brand = models.ForeignKey(
        SensorBrand,
        on_delete=models.PROTECT,
        verbose_name="Sensor brand",
        null=True,
        help_text="Sensor brand.",
    )
    model = models.CharField(
        "Model",
        max_length=150,
        null=True,
        blank=True,
        help_text="Specific model of the sensor.",
    )
    serial = models.CharField(
        "Serial number",
        max_length=20,
        null=True,
        blank=True,
        help_text="Serial number of the sensor.",
    )
    status = models.BooleanField(
        "Status (active)", default=False, help_text="If the sensor is active."
    )

    def __str__(self) -> str:
        """Return the sensor code."""
        return str(self.code)

    def get_absolute_url(self) -> str:
        """Return the absolute url of the sensor."""
        return reverse("sensor:sensor_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = (
            "code",
            "sensor_type",
            "sensor_brand",
            "model",
        )
