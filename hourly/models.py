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

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from timescale.db.models.models import TimescaleModel

from station.models import Station

HOURLYS: List[str] = []
"""Available hourly variables."""


# TODO check if PolarWind is needed in HOurly
class PolarWind(TimescaleModel):
    """
    Polar Wind hourly with a velocity and direction at a specific time.
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


class BaseHourly(TimescaleModel):
    @classmethod
    def __init_subclass__(cls, *args, **kwargs) -> None:
        if not cls.__name__.startswith("_Hour") and cls.__name__ not in HOURLYS:
            HOURLYS.append(cls.__name__)

    time = models.DateTimeField()
    station_id = models.PositiveIntegerField("station_id")
    used_for_daily = models.BooleanField("used_for_daily", default=False)
    completeness = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        abstract = True

    # TODO Check if this is wanted/needed
    def clean(self):
        super().clean()
        if self.time.minute or self.time.second:
            raise ValidationError(
                "The information of minutes and seconds is not allowed in this field."
            )

    # TODO check if this is wanted/needed
    def save(self, *args, **kwargs):
        self.time = self.time.replace(minute=0, second=0, microsecond=0)
        super().save(*args, **kwargs)


def create_hour_model(
    digits=14, decimals=6, fields=("Average",)
) -> Type[TimescaleModel]:
    num = len(HOURLYS) + 1
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
            models.Index(fields=["used_for_daily"]),
            models.Index(fields=["station_id", "time"]),
            models.Index(fields=["time", "station_id"]),
        ]

    attrs = {"__module__": __name__, "Meta": Meta}
    attrs.update(_fields)

    return type(
        f"_Hour{num}",
        (BaseHourly,),
        attrs,
    )


class Precipitation(create_hour_model(digits=6, decimals=2, fields=("Sum",))):
    """Precipitation."""


class AirTemperature(create_hour_model(digits=5, decimals=2)):
    """Air temperature."""


class Humidity(create_hour_model()):
    """Humidity."""


class WindVelocity(create_hour_model()):
    """Wind velocity."""


class WindDirection(create_hour_model()):
    """Wind direction."""


class SoilMoisture(create_hour_model()):
    """Soil moisture."""


class SolarRadiation(create_hour_model()):
    """Solar radiation."""


class AtmosphericPressure(create_hour_model()):
    """Atmospheric pressure."""


class WaterTemperature(create_hour_model()):
    """Water temperature."""


class Flow(create_hour_model()):
    """Flow."""


class WaterLevel(create_hour_model()):
    """Water level."""


class BatteryVoltage(create_hour_model()):
    """Battery voltage."""


# TODO Check if this variable wouldn´t have table in hourly, daily and MOnthly
class FlowManual(create_hour_model(fields=("Value",))):
    """Flow (manual)."""


# TODO Check if There is needed StripLevelReading hourly.
class StripLevelReading(create_hour_model(fields=("Value", "Uncertainty"))):
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


class SoilTemperature(create_hour_model()):
    """Soil temperature."""


class IndirectRadiation(create_hour_model()):
    """Indirect radiation."""


# Variables created for buoy with different depths
class WaterTemperatureDepth(
    create_hour_model(
        digits=6,
        decimals=2,
    ),
):
    """Water temperature (degrees celcius) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class WaterAcidityDepth(
    create_hour_model(
        digits=6,
        decimals=2,
    ),
):
    """Water acidity (pH) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class RedoxPotentialDepth(
    create_hour_model(
        digits=6,
        decimals=2,
    ),
):
    """Redox potential (mV) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class WaterTurbidityDepth(
    create_hour_model(
        digits=6,
        decimals=2,
    ),
):
    """Water turbidity (NTU) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class ChlorineConcentrationDepth(
    create_hour_model(
        digits=6,
        decimals=2,
    ),
):
    """Chlorine concentration (ug/l) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class OxygenConcentrationDepth(
    create_hour_model(
        digits=6,
        decimals=2,
    ),
):
    """Oxygen concentration (mg/l) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class PercentageOxygenConcentrationDepth(
    create_hour_model(
        digits=6,
        decimals=2,
    ),
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
    create_hour_model(
        digits=6,
        decimals=2,
    ),
):
    """Phycocyanin (?) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]
