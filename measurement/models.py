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
        Station, on_delete=models.CASCADE, null=False, verbose_name="Station"
    )
    variable = models.ForeignKey(
        Variable, on_delete=models.PROTECT, null=False, verbose_name="Variable"
    )
    value = models.DecimalField("value", max_digits=14, decimal_places=6, null=False)
    maximum = models.DecimalField(
        "maximum", max_digits=14, decimal_places=6, null=True, blank=True
    )
    minimum = models.DecimalField(
        "minimum", max_digits=14, decimal_places=6, null=True, blank=True
    )

    class Meta:
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
    completeness = models.DecimalField(max_digits=4, decimal_places=1, null=False)

    class Meta:
        indexes = [
            models.Index(fields=["report_type", "station", "time", "variable"]),
        ]

    def clean(self) -> None:
        """Validate that the report type and use of the data is consistent."""
        if self.report_type == ReportType.HOURLY:
            self.time = self.time.replace(minute=0, second=0, microsecond=0)
        elif self.report_type == ReportType.DAILY:
            self.time = self.time.replace(hour=0, minute=0, second=0, microsecond=0)
        elif self.report_type == ReportType.MONTLY:
            self.time = self.time.replace(
                day=1, hour=0, minute=0, second=0, microsecond=0
            )


class Measurement(MeasurementBase):
    """Class to store the measurements and their validation status.

    This class holds the value of a given variable and station at a specific time, as
    well as auxiliary information such as maximum and minimum values, depth and
    direction, for vector quantities. All of these hava a `raw` version where a backup
    of the original data is kept, should this change at any point.

    Flags to monitor its validation status, if the data is active (and therefore can be
    used for reporting) and if it has actually been used for that is also included.
    """

    depth = models.PositiveSmallIntegerField("depth", null=True, blank=True)
    direction = models.DecimalField(
        "direction", max_digits=14, decimal_places=6, null=True, blank=True
    )
    raw_value = models.DecimalField(
        "raw value",
        max_digits=14,
        decimal_places=6,
        null=True,
        blank=True,
        editable=False,
    )
    raw_maximum = models.DecimalField(
        "raw maximum",
        max_digits=14,
        decimal_places=6,
        null=True,
        blank=True,
        editable=False,
    )
    raw_minimum = models.DecimalField(
        "raw minimum",
        max_digits=14,
        decimal_places=6,
        null=True,
        blank=True,
        editable=False,
    )
    raw_direction = models.DecimalField(
        "raw direction",
        max_digits=14,
        decimal_places=6,
        null=True,
        blank=True,
        editable=False,
    )
    raw_depth = models.PositiveSmallIntegerField(
        "raw depth", null=True, blank=True, editable=False
    )
    is_validated = models.BooleanField("Validated?", default=False)
    is_active = models.BooleanField("Active?", default=True)

    def clean(self) -> None:
        """Check consistency of validation, reporting and backs-up values."""
        # Check consistency of validation
        if not self.is_validated and not self.is_active:
            raise ValidationError("Only validated entries can be delcared as inactive.")

        # Backup values to raws, if needed
        raws = (r for r in dir(self) if r.startswith("raw_"))
        for r in raws:
            value = getattr(self, r.removeprefix("raw_"))
            if value and not getattr(self, r):
                setattr(self, r, value)

    @property
    def overwritten(self) -> bool:
        """Indicates if any of the values associated to the entry have been overwritten.

        Returns:
            bool: True if any raw field is different to the corresponding standard
                field.
        """
        raws = (r for r in dir(self) if r.startswith("raw_"))
        for r in raws:
            value = getattr(self, r.removeprefix("raw_"))
            if value and value != getattr(self, r):
                return True

        return False
