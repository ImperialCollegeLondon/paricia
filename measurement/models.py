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

from typing import Type, List

from django.db import models
from django.urls import reverse

from station.models import Station


MEASUREMENTS: List[str] = []
"""Available measurent variables."""


class PermissionsMeasurement(models.Model):
    """
    Model used to define the permission "validar".
    """

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (("validar", "usar interfaz de validación"),)


class PolarWind(models.Model):
    """
    Polar Wind measurement with a velocity and direction at a specific date.
    """

    date = models.DateTimeField("Date")
    speed = models.DecimalField("Speed", max_digits=14, decimal_places=6, null=True)
    direction = models.DecimalField(
        "Direction", max_digits=14, decimal_places=6, null=True
    )

    class Meta:
        """
        Para que no se cree en la migracion.

        NOTE: Why don't we want this in the migration?
        """

        default_permissions = ()
        managed = False


class DischargeCurve(models.Model):
    """
    Discharge curve.

    Relates a station and a date and a bool as to whether a flow recalculation is
    required.
    """

    id = models.AutoField("Id", primary_key=True)
    station = models.ForeignKey(
        Station, on_delete=models.SET_NULL, null=True, verbose_name="Station"
    )
    date = models.DateTimeField("Date")
    require_recalculate_flow = models.BooleanField(
        verbose_name="Requires re-calculate flow?", default=False
    )

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse("measurement:dischargecurve_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("station", "date")
        unique_together = ("station", "date")


class LevelFunction(models.Model):
    """
    Function Level. Relates a discharge curve to a level (in cm) to a function.

    NOTE: No idea what this is -> Ask Pablo
    """

    discharge_curve = models.ForeignKey(DischargeCurve, on_delete=models.CASCADE)
    level = models.DecimalField(
        "Level (cm)", max_digits=5, decimal_places=1, db_index=True
    )
    function = models.CharField("Function", max_length=80)

    def __str__(self):
        return str(self.pk)

    def get_absolute_url(self):
        return reverse("measurement:levelfunction_detail", kwargs={"pk": self.pk})

    class Meta:
        default_permissions = ()
        ordering = (
            "discharge_curve",
            "level",
        )


##############################################################


class BaseMeasurement(models.Model):
    @classmethod
    def __init_subclass__(cls, *args, **kwargs) -> None:
        if cls.__name__ not in MEASUREMENTS:
            MEASUREMENTS.append(cls.__name__)

    station_id = models.PositiveIntegerField("station_id")
    date = models.DateTimeField("Date")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "date"]),
            models.Index(fields=["date", "station_id"]),
        ]
        abstract = True


def custom_meas_model(
    digits=14, decimals=6, fields=("Value", "Maximum", "Minimum")
) -> Type[models.Model]:
    num = len(MEASUREMENTS) + 1
    _fields = {
        key.lower(): models.DecimalField(
            key,
            max_digits=digits,
            decimal_places=decimals,
            null=True,
        )
        for key in fields
    }

    return type(
        f"Limits{num}", (models.Model,), {"field": _fields, "__module__": __name__}
    )


class Precipitation(
    BaseMeasurement, custom_meas_model(digits=6, decimals=2, fields=("Value"))
):
    """Precipitation."""


class AirTemperature(BaseMeasurement, custom_meas_model(digits=5, decimals=2)):
    """Air temperature."""


class Humidity(BaseMeasurement, custom_meas_model()):
    """Humidity."""


class WindVelocity(BaseMeasurement, custom_meas_model()):
    """Wind velocity."""


class WindDirection(BaseMeasurement, custom_meas_model()):
    """Wind direction."""


class SoilMoisture(BaseMeasurement, custom_meas_model()):
    """Soil moisture."""


class SolarRadiation(BaseMeasurement, custom_meas_model()):
    """Solar radiation."""


class AtmosphericPressure(BaseMeasurement, custom_meas_model()):
    """Atmospheric pressure."""


class WaterTemperature(BaseMeasurement, custom_meas_model()):
    """Water temperature."""


class Flow(BaseMeasurement, custom_meas_model()):
    """Flow."""


class WaterLevel(BaseMeasurement, custom_meas_model()):
    """Water level."""


class BatteryVoltage(BaseMeasurement, custom_meas_model()):
    """Battery voltage."""


class FlowManual(BaseMeasurement, custom_meas_model(fields=("Value"))):
    """Flow (manual)."""


class Var14Measurement(
    BaseMeasurement, custom_meas_model(fields=("Value", "Uncertainty"))
):
    """Fix: Need proper name"""

    data_import_date = models.DateTimeField("Data import date")
    data_start_date = models.DateTimeField("Data start date")
    calibrated = models.BooleanField("Calibrated")
    comments = models.CharField("Comments", null=True, max_length=250)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "data_import_date"]),
            models.Index(fields=["station_id", "data_start_date", "date"]),
            models.Index(fields=["data_import_date"]),
        ]


class SoilTemperature(BaseMeasurement, custom_meas_model()):
    """Soil temperature."""


class IndirectRadiation(BaseMeasurement, custom_meas_model()):
    """Indirect radiation."""


# Variables created for buoy with different depths


class WaterTemperature(
    BaseMeasurement,
    custom_meas_model(digits=6, decimals=2, fields=("Value")),
):
    """Water temperature (degrees celcius) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]


class WaterAcidity(
    BaseMeasurement,
    custom_meas_model(digits=6, decimals=2, fields=("Value")),
):
    """Water acidity (pH) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]


class RedoxPotential(
    BaseMeasurement,
    custom_meas_model(digits=6, decimals=2, fields=("Value")),
):
    """Redox potential (mV) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]


class WaterTurbidity(
    BaseMeasurement,
    custom_meas_model(digits=6, decimals=2, fields=("Value")),
):
    """Water turbidity (NTU) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]


class ClorineConcentration(
    BaseMeasurement,
    custom_meas_model(digits=6, decimals=2, fields=("Value")),
):
    """Chlorine concentration (ug/l) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]


class OxigenConcentration(
    BaseMeasurement,
    custom_meas_model(digits=6, decimals=2, fields=("Value")),
):
    """Oxygen concentration (mg/l) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]


class PercentageOxigenConcentration(
    BaseMeasurement,
    custom_meas_model(digits=6, decimals=2, fields=("Value")),
):
    """Percentage oxygen concentration (mg/l) at a depth in cm.

    HELPWANTED: Is this wrong? It's teh same as above, perhaps units should
    be %? --> DIEGO: Looks identical to the previous one to me. It might be an error.
    """

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]


class Phycocyanin(
    BaseMeasurement,
    custom_meas_model(digits=6, decimals=2, fields=("Value")),
):
    """Phycocyanin (?) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "date"]),
        ]
