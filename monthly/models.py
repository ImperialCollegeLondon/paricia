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
from django.core.exceptions import ValidationError

from station.models import Station

MONTHLYS: List[str] = []
"""Available monthly variables."""

# TODO check if PolarWind is needed in monthly
class PolarWind(TimescaleModel):
    """
    Polar Wind monthly with a velocity and direction at a specific time.
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




class BaseMonthly(TimescaleModel):
    @classmethod
    def __init_subclass__(cls, *args, **kwargs) -> None:
        if not cls.__name__.startswith("_Mon") and cls.__name__ not in MONTHLYS:
            MONTHLYS.append(cls.__name__)

    # TODO ask if "date" name is OK
    # TODO ask if default=timezone.now is OK,
    # date = models.DateField(default=timezone.now)
    date = models.DateField("date")
    station_id = models.PositiveIntegerField("station_id")
    completeness = models.DecimalField(max_digits=4, decimal_places=1)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["used_for_monthly"]),
            models.Index(fields=["station_id", "time"]),
            models.Index(fields=["time", "station_id"]),
        ]
        abstract = True


def create_Mon_model(
    digits=14, decimals=6, fields=("Average")
) -> Type[TimescaleModel]:
    num = len(MONTHLYS) + 1
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

    attrs = {"__module__": __name__, "Meta": Meta}
    attrs.update(_fields)

    return type(
        f"_Mon{num}",
        (BaseMonthly,),
        attrs,
    )


class Precipitation(create_Mon_model(digits=6, decimals=2, fields=("Total",))):
    """Precipitation."""


class AirTemperature(create_Mon_model(digits=5, decimals=2)):
    """Air temperature."""


class Humidity(create_Mon_model()):
    """Humidity."""


class WindVelocity(create_Mon_model()):
    """Wind velocity."""


class WindDirection(create_Mon_model()):
    """Wind direction."""


class SoilMoisture(create_Mon_model()):
    """Soil moisture."""


class SolarRadiation(create_Mon_model()):
    """Solar radiation."""


class AtmosphericPressure(create_Mon_model()):
    """Atmospheric pressure."""


class WaterTemperature(create_Mon_model()):
    """Water temperature."""


class Flow(create_Mon_model()):
    """Flow."""


class WaterLevel(create_Mon_model()):
    """Water level."""


class BatteryVoltage(create_Mon_model()):
    """Battery voltage."""


class FlowManual(create_Mon_model(fields=("Value",))):
    """Flow (manual)."""


# TODO Check if There id needed StripLevelReading monthly.
class StripLevelReading(create_Mon_model(fields=("Value", "Uncertainty"))):
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


class SoilTemperature(create_Mon_model()):
    """Soil temperature."""


class IndirectRadiation(create_Mon_model()):
    """Indirect radiation."""


# Variables created for buoy with different depths
class WaterTemperatureDepth(
    create_Mon_model(digits=6, decimals=2,),
):
    """Water temperature (degrees celcius) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class WaterAcidityDepth(
    create_Mon_model(digits=6, decimals=2,),
):
    """Water acidity (pH) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class RedoxPotentialDepth(
    create_Mon_model(digits=6, decimals=2, ),
):
    """Redox potential (mV) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class WaterTurbidityDepth(
    create_Mon_model(digits=6, decimals=2, ),
):
    """Water turbidity (NTU) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class ChlorineConcentrationDepth(
    create_Mon_model(digits=6, decimals=2, ),
):
    """Chlorine concentration (ug/l) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class OxygenConcentrationDepth(
    create_Mon_model(digits=6, decimals=2, ),
):
    """Oxygen concentration (mg/l) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class PercentageOxygenConcentrationDepth(
    create_Mon_model(digits=6, decimals=2, ),
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
    create_Mon_model(digits=6, decimals=2, ),
):
    """Phycocyanin (?) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]
