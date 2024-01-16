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
from variable.models import Variable

MEASUREMENTS: List[str] = []
"""Available measurement variables."""


class MeasurementBase(TimescaleModel):
    """Base class for all the measurement related entries.

    It contains the barebone attributes that any measurement entry will likely need,
    although this is enforced only for station, variable and value. Maximum and minimum
    are very likely to be present in most cases, but might not be there in some
    occasions, therefore the possibility of nulling them.
    """

    station = models.ForeignKey(
        Station, on_delete=models.PROTECT, null=False, verbose_name="Station"
    )
    variable = models.ForeignKey(
        Variable, on_delete=models.PROTECT, null=False, verbose_name="Variable"
    )
    value = models.DecimalField(
        "value",
        max_digits=14,
        decimal_places=6,
        null=False,
    )
    maximum = models.DecimalField(
        "maximum",
        max_digits=14,
        decimal_places=6,
        null=True,
    )
    minimum = models.DecimalField(
        "minimum",
        max_digits=14,
        decimal_places=6,
        null=True,
    )

    class Meta:
        default_permissions = ()
        abstract = True
        indexes = [
            models.Index(fields=["station", "time", "variable"]),
        ]


class ReportType(models.TextChoices):
    HOURLY = "hourly"
    DAILY = "daily"
    MONTLY = "monthly"


class Report(MeasurementBase):
    """Holds the different reporting data.

    It also keeps track of which data has already been used when creating the reports.
    """

    report_type = models.CharField(max_length=7, choices=ReportType.choices, null=False)
    used_for_daily = models.BooleanField(
        verbose_name="Has data been used already for a daily report?", default=False
    )
    used_for_monthly = models.BooleanField(
        verbose_name="Has data been used already for a montly report?", default=False
    )

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["report_type", "station", "time", "variable"]),
        ]

    def clean(self) -> None:
        """Validate that the report type and use of the data is consistent."""
        if self.used_for_daily and self.report_type != ReportType.HOURLY:
            raise ValueError(
                "Only hourly data can be used for daily report calculations."
            )
        if self.used_for_monthly and self.report_type != ReportType.DAILY:
            raise ValueError(
                "Only daily data can be used for monthly report calculations."
            )


## Legacy models - to be removed


class PermissionsMeasurement(models.Model):
    """
    Model used to define the permission "validar".
    """

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (("validar", "usar interfaz de validación"),)


class PolarWind(TimescaleModel):
    """
    Polar Wind measurement with a velocity and direction at a specific time.
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


class DischargeCurve(TimescaleModel):
    """
    Discharge curve.

    Relates a station and a time and a bool as to whether a flow recalculation is
    required.
    """

    id = models.AutoField("Id", primary_key=True)
    station = models.ForeignKey(
        Station, on_delete=models.SET_NULL, null=True, verbose_name="Station"
    )
    require_recalculate_flow = models.BooleanField(
        verbose_name="Requires re-calculate flow?", default=False
    )

    def __str__(self):
        return self.id

    def get_absolute_url(self):
        return reverse("measurement:dischargecurve_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("station", "time")
        unique_together = ("station", "time")


class LevelFunction(TimescaleModel):
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


class BaseMeasurement(TimescaleModel):
    @classmethod
    def __init_subclass__(cls, *args, **kwargs) -> None:
        if not cls.__name__.startswith("_Meas") and cls.__name__ not in MEASUREMENTS:
            MEASUREMENTS.append(cls.__name__)

    station_id = models.PositiveIntegerField("station_id")

    class Meta:
        default_permissions = ()
        abstract = True


def create_meas_model(
    digits=14, decimals=6, fields=("Average", "Maximum", "Minimum")
) -> Type[TimescaleModel]:
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

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=["station_id", "time"]),
            models.Index(fields=["time", "station_id"]),
        ]

    attrs = {"__module__": __name__, "Meta": Meta}
    attrs.update(_fields)

    return type(
        f"_Meas{num}",
        (BaseMeasurement,),
        attrs,
    )


# TODO Tell that tables (i.e. measurement_precipitation) are not inheriting indexes on multiple columns
#  They only present primary key index
# By the way, Models has explicit index (i.e. WaterTemperatureDepth) shows those indexes in the database
class Precipitation(create_meas_model(digits=6, decimals=2, fields=("Sum",))):
    """Precipitation."""


class AirTemperature(create_meas_model(digits=5, decimals=2)):
    """Air temperature."""


class Humidity(create_meas_model()):
    """Humidity."""


class WindVelocity(create_meas_model()):
    """Wind velocity."""


class WindDirection(create_meas_model()):
    """Wind direction."""


class SoilMoisture(create_meas_model()):
    """Soil moisture."""


class SolarRadiation(create_meas_model()):
    """Solar radiation."""


class AtmosphericPressure(create_meas_model()):
    """Atmospheric pressure."""


class WaterTemperature(create_meas_model()):
    """Water temperature."""


class Flow(create_meas_model()):
    """Flow."""


class WaterLevel(create_meas_model()):
    """Water level."""


class BatteryVoltage(create_meas_model()):
    """Battery voltage."""


class FlowManual(create_meas_model(fields=("Average",))):
    """Flow (manual)."""


class StripLevelReading(create_meas_model(fields=("Value", "Uncertainty"))):
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


class SoilTemperature(create_meas_model()):
    """Soil temperature."""


class IndirectRadiation(create_meas_model()):
    """Indirect radiation."""


# Variables created for buoy with different depths
class WaterTemperatureDepth(
    create_meas_model(digits=6, decimals=2, fields=("Average",)),
):
    """Water temperature (degrees celcius) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class WaterAcidityDepth(
    create_meas_model(digits=6, decimals=2, fields=("Average",)),
):
    """Water acidity (pH) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class RedoxPotentialDepth(
    create_meas_model(digits=6, decimals=2, fields=("Average",)),
):
    """Redox potential (mV) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class WaterTurbidityDepth(
    create_meas_model(digits=6, decimals=2, fields=("Average",)),
):
    """Water turbidity (NTU) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class ChlorineConcentrationDepth(
    create_meas_model(digits=6, decimals=2, fields=("Average",)),
):
    """Chlorine concentration (ug/l) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class OxygenConcentrationDepth(
    create_meas_model(digits=6, decimals=2, fields=("Average",)),
):
    """Oxygen concentration (mg/l) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]


class PercentageOxygenConcentrationDepth(
    create_meas_model(digits=6, decimals=2, fields=("Average",)),
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
    create_meas_model(digits=6, decimals=2, fields=("Average",)),
):
    """Phycocyanin (?) at a depth in cm."""

    depth = models.PositiveSmallIntegerField("Depth")

    class Meta:
        default_permissions = ()
        indexes = [
            models.Index(fields=["station_id", "depth", "time"]),
        ]
