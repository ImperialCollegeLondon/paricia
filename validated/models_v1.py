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

from station.models import Station

VALIDATEDS: List[str] = []
"""Available validated variables."""


# class PermissionsValidated(models.Model):
#     """
#     Model used to define the permission "validar".
#     """
#
#     class Meta:
#         managed = False
#         default_permissions = ()
#         permissions = (("validar", "usar interfaz de validación"),)


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


# class DischargeCurve(TimescaleModel):
#     """
#     Discharge curve.
# 
#     Relates a station and a time and a bool as to whether a flow recalculation is
#     required.
#     """
# 
#     id = models.AutoField("Id", primary_key=True)
#     station = models.ForeignKey(
#         Station, on_delete=models.SET_NULL, null=True, verbose_name="Station"
#     )
#     require_recalculate_flow = models.BooleanField(
#         verbose_name="Requires re-calculate flow?", default=False
#     )
# 
#     def __str__(self):
#         return self.id
# 
#     def get_absolute_url(self):
#         return reverse("validated:dischargecurve_detail", kwargs={"pk": self.pk})
# 
#     class Meta:
#         ordering = ("station", "time")
#         unique_together = ("station", "time")


# class LevelFunction(TimescaleModel):
#     """
#     Function Level. Relates a discharge curve to a level (in cm) to a function.
# 
#     NOTE: No idea what this is -> Ask Pablo
#     """
# 
#     discharge_curve = models.ForeignKey(DischargeCurve, on_delete=models.CASCADE)
#     level = models.DecimalField(
#         "Level (cm)", max_digits=5, decimal_places=1, db_index=True
#     )
#     function = models.CharField("Function", max_length=80)
# 
#     def __str__(self):
#         return str(self.pk)
# 
#     def get_absolute_url(self):
#         return reverse("validated:levelfunction_detail", kwargs={"pk": self.pk})
# 
#     class Meta:
#         default_permissions = ()
#         ordering = (
#             "discharge_curve",
#             "level",
#         )


##############################################################


class BaseValidated(TimescaleModel):
    @classmethod
    def __init_subclass__(cls, *args, **kwargs) -> None:
        if not cls.__name__.startswith("_Vali") and cls.__name__ not in VALIDATEDS:
            VALIDATEDS.append(cls.__name__)

    station_id = models.PositiveIntegerField("station_id")
    # TODO check
    used_for_hourly = models.BooleanField("used_for_hourly", default=False)

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["used_for_hourly"]),
            models.Index(fields=["station_id", "time"]),
            models.Index(fields=["time", "station_id"]),
        ]
        abstract = True


def create_vali_model(
    digits=14, decimals=6, fields=("Value", "Maximum", "Minimum")
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

    attrs = {"__module__": __name__, "Meta": Meta}
    attrs.update(_fields)

    return type(
        f"_Vali{num}",
        (BaseValidated,),
        attrs,
    )


class Precipitation(create_vali_model(digits=6, decimals=2, fields=("Value",))):
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


class FlowManual(create_vali_model(fields=("Value",))):
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
    create_vali_model(digits=6, decimals=2, fields=("Value",)),
):
    """Water temperature (degrees celcius) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class WaterAcidityDepth(
    create_vali_model(digits=6, decimals=2, fields=("Value",)),
):
    """Water acidity (pH) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class RedoxPotentialDepth(
    create_vali_model(digits=6, decimals=2, fields=("Value",)),
):
    """Redox potential (mV) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class WaterTurbidityDepth(
    create_vali_model(digits=6, decimals=2, fields=("Value",)),
):
    """Water turbidity (NTU) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class ChlorineConcentrationDepth(
    create_vali_model(digits=6, decimals=2, fields=("Value",)),
):
    """Chlorine concentration (ug/l) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class OxygenConcentrationDepth(
    create_vali_model(digits=6, decimals=2, fields=("Value",)),
):
    """Oxygen concentration (mg/l) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class PercentageOxygenConcentrationDepth(
    create_vali_model(digits=6, decimals=2, fields=("Value",)),
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
    create_vali_model(digits=6, decimals=2, fields=("Value",)),
):
    """Phycocyanin (?) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]
