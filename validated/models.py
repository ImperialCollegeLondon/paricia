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

from typing import List, Type

from django.db import models
from django.urls import reverse
from timescale.db.models.models import TimescaleModel

import measurement.models as meas
from station.models import Station

VALIDATEDS: List[str] = []
"""Available validated variables."""

# class Permissions(models.Model):
#
#     class Meta:
#         managed = False
#         default_permissions = ()
#         permissions = (
#             ('daily_validation', 'Permission for validate raw data.')
#         )


class PolarWind(TimescaleModel):
    """
    Polar Wind validated with a velocity and direction at a specific time.
    """

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


class BaseValidated(TimescaleModel):
    @classmethod
    def __init_subclass__(cls, *args, **kwargs) -> None:
        if not cls.__name__.startswith("_Vali") and cls.__name__ not in VALIDATEDS:
            VALIDATEDS.append(cls.__name__)

    station_id = models.PositiveIntegerField("station_id")
    used_for_hourly = models.BooleanField("used_for_hourly", default=False)

    class Meta:
        default_permissions = ()
        abstract = True


def create_vali_model(
    digits=14, decimals=6, fields=("Average", "Maximum", "Minimum")
) -> Type[TimescaleModel]:
    num = len(VALIDATEDS) + 1
    _fields = {
        key.lower(): models.DecimalField(
            key,
            max_digits=digits,
            decimal_places=decimals,
            null=True,
        )
        for key in fields
    }

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["used_for_hourly"]),
            models.Index(fields=["station_id", "time"]),
            models.Index(fields=["time", "station_id"]),
        ]

    attrs = {"__module__": __name__, "Meta": Meta}
    attrs.update(_fields)

    return type(
        f"_Vali{num}",
        (BaseValidated,),
        attrs,
    )


# TODO Copy the decimal_places and max_digits from a measurement model
# meas.Precipitation._meta.get_field('Value').max_digits
# meas.Precipitation._meta.get_field('Value').decimal_places
class Precipitation(create_vali_model(digits=6, decimals=2, fields=("Sum",))):
    """Precipitation."""


class AirTemperature(create_vali_model(digits=5, decimals=2)):
    """Air temperature."""


class Humidity(create_vali_model()):
    """Humidity."""


class WindVelocity(create_vali_model()):
    """Wind velocity."""


class WindDirection(create_vali_model()):
    """Wind direction."""


class SoilMoisture(create_vali_model()):
    """Soil moisture."""


class SolarRadiation(create_vali_model()):
    """Solar radiation."""


class AtmosphericPressure(create_vali_model()):
    """Atmospheric pressure."""


class WaterTemperature(create_vali_model()):
    """Water temperature."""


class Flow(create_vali_model()):
    """Flow."""


class WaterLevel(create_vali_model()):
    """Water level."""


class BatteryVoltage(create_vali_model()):
    """Battery voltage."""


class FlowManual(create_vali_model(fields=("Average",))):
    """Flow (manual)."""


# TODO Check if There id needed StripLevelReading validated.
class StripLevelReading(create_vali_model(fields=("Value", "Uncertainty"))):
    """Strip level reading."""

    data_import_date = models.DateTimeField("Data import date")
    data_start_date = models.DateTimeField("Data start date")
    calibrated = models.BooleanField("Calibrated")
    comments = models.CharField("Comments", null=True, max_length=250)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "data_import_date"]),
            models.Index(fields=["station_id", "data_start_date", "time"]),
            models.Index(fields=["data_import_date"]),
        ]


class SoilTemperature(create_vali_model()):
    """Soil temperature."""


class IndirectRadiation(create_vali_model()):
    """Indirect radiation."""


# Variables created for buoy with different depths
class WaterTemperatureDepth(
    create_vali_model(digits=6, decimals=2, fields=("Average",)),
):
    """Water temperature (degrees celcius) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class WaterAcidityDepth(
    create_vali_model(digits=6, decimals=2, fields=("Average",)),
):
    """Water acidity (pH) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class RedoxPotentialDepth(
    create_vali_model(digits=6, decimals=2, fields=("Average",)),
):
    """Redox potential (mV) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class WaterTurbidityDepth(
    create_vali_model(digits=6, decimals=2, fields=("Average",)),
):
    """Water turbidity (NTU) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class ChlorineConcentrationDepth(
    create_vali_model(digits=6, decimals=2, fields=("Average",)),
):
    """Chlorine concentration (ug/l) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class OxygenConcentrationDepth(
    create_vali_model(digits=6, decimals=2, fields=("Average",)),
):
    """Oxygen concentration (mg/l) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class PercentageOxygenConcentrationDepth(
    create_vali_model(digits=6, decimals=2, fields=("Average",)),
):
    """Percentage oxygen concentration (mg/l) at a depth in cm.

    HELPWANTED: Is this wrong? It's teh same as above, perhaps units should
    be %? --> DIEGO: Looks identical to the previous one to me. It might be an error.
    """

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class PhycocyaninDepth(
    create_vali_model(digits=6, decimals=2, fields=("Average",)),
):
    """Phycocyanin (?) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]