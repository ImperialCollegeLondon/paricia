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


from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from timescale.db.models.models import TimescaleDateTimeField, TimescaleModel

from management.models import apply_add_permissions_to_standard_group
from station.models import Station
from variable.models import Variable

MEASUREMENTS: list[str] = []
"""Available measurement variables."""


class MeasurementBase(TimescaleModel):
    """Base class for all the measurement related entries.

    It contains the barebone attributes that any measurement entry will likely need,
    although this is enforced only for station, variable and value. Maximum and minimum
    are very likely to be present in most cases, but might not be there in some
    occasions, therefore the possibility of nulling them.

    Attributes:
        time (TimescaleDateTimeField): Time of the measurement.
        station (Station): Station this measurement belongs to.
        variable (Variable): Variable being measured.
        value (Decimal): Value of the measurement.
        maximum (Decimal): Maximum value of the measurement. Mostly useful for reports
            or when the measurement represents an average over time.
        minimum (Decimal): Minimum value of the measurement. Mostly useful for reports
            or when the measurement represents an average over time.
    """

    time: TimescaleDateTimeField

    station = models.ForeignKey(
        Station,
        on_delete=models.PROTECT,
        null=False,
        verbose_name="Station",
        help_text="Station this measurement belongs to.",
    )
    variable = models.ForeignKey(
        Variable,
        on_delete=models.PROTECT,
        null=False,
        verbose_name="Variable",
        help_text="Variable being measured.",
    )
    value = models.DecimalField(
        "value",
        max_digits=14,
        decimal_places=6,
        null=False,
        help_text="Value of the measurement.",
    )
    maximum = models.DecimalField(
        "maximum",
        max_digits=14,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Maximum value of the measurement. Mostly useful for reports or when "
        "the measurement represents an average over time.",
    )
    minimum = models.DecimalField(
        "minimum",
        max_digits=14,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Minimum value of the measurement. Mostly useful for reports or when "
        "the measurement represents an average over time.",
    )

    @classmethod
    def set_model_permissions(cls) -> None:
        """Set model-level add permissions."""
        apply_add_permissions_to_standard_group(cls)

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

    Attributes:
        report_type (str): Type of report. It can be hourly, daily or monthly.
        completeness (Decimal): Completeness of the report. Eg. a daily report with 24
            hourly measurements would have a completeness of 100%.
    """

    report_type = models.CharField(
        max_length=7,
        choices=ReportType.choices,
        null=False,
        help_text="Type of report. It can be hourly, daily or monthly.",
    )
    completeness = models.DecimalField(
        max_digits=4,
        decimal_places=1,
        default=100,
        null=False,
        help_text="Completeness of the report. Eg. a daily report made out of 24 hourly"
        " measurements would have a completeness of 100%.",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )

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
    direction, for vector quantities. All of these have a `raw` version where a backup
    of the original data is kept, should this change at any point.

    Flags to monitor its validation status, if the data is active (and therefore can be
    used for reporting) and if it has actually been used for that is also included.

    Attributes:
        depth (int): Depth of the measurement.
        direction (Decimal): Direction of the measurement, useful for vector quantities.
        raw_value (Decimal): Original value of the measurement.
        raw_maximum (Decimal): Original maximum value of the measurement.
        raw_minimum (Decimal): Original minimum value of the measurement.
        raw_direction (Decimal): Original direction of the measurement.
        raw_depth (int): Original depth of the measurement.
        is_validated (bool): Flag to indicate if the measurement has been validated.
        is_active (bool): Flag to indicate if the measurement is active. An inactive
            measurement is not used for reporting
    """

    depth = models.PositiveSmallIntegerField(
        "depth", null=True, blank=True, help_text="Depth of the measurement."
    )
    direction = models.DecimalField(
        "direction",
        max_digits=14,
        decimal_places=6,
        null=True,
        blank=True,
        help_text="Direction of the measurement, useful for vector quantities. It "
        "should be a number in the [0, 360) interval, where 0 represents north.",
    )
    raw_value = models.DecimalField(
        "raw value",
        max_digits=14,
        decimal_places=6,
        null=True,
        blank=True,
        editable=False,
        help_text="Original value of the measurement.",
    )
    raw_maximum = models.DecimalField(
        "raw maximum",
        max_digits=14,
        decimal_places=6,
        null=True,
        blank=True,
        editable=False,
        help_text="Original maximum value of the measurement.",
    )
    raw_minimum = models.DecimalField(
        "raw minimum",
        max_digits=14,
        decimal_places=6,
        null=True,
        blank=True,
        editable=False,
        help_text="Original minimum value of the measurement.",
    )
    raw_direction = models.DecimalField(
        "raw direction",
        max_digits=14,
        decimal_places=6,
        null=True,
        blank=True,
        editable=False,
        help_text="Original direction of the measurement.",
    )
    raw_depth = models.PositiveSmallIntegerField(
        "raw depth",
        null=True,
        blank=True,
        editable=False,
        help_text="Original depth of the measurement.",
    )
    is_validated = models.BooleanField(
        "Validated?",
        default=False,
        help_text="Flag to indicate if the measurement has been validated.",
    )
    is_active = models.BooleanField(
        "Active?",
        default=True,
        help_text="Flag to indicate if the measurement is active. An inactive "
        "measurement is not used for reporting.",
    )

    @property
    def raws(self) -> tuple[str, ...]:
        """Return the raw fields of the measurement.

        Returns:
            tuple[str]: Tuple with the names of the raw fields of the measurement.
        """
        return tuple([r for r in dir(self) if r.startswith("raw_")])

    def clean(self) -> None:
        """Check consistency of validation, reporting and backs-up values."""
        # Check consistency of validation
        if not self.is_validated and not self.is_active:
            raise ValidationError("Only validated entries can be declared as inactive.")

        # Backup values to raws, if needed
        for r in self.raws:
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
        for r in self.raws:
            value = getattr(self, r.removeprefix("raw_"))
            if value and value != getattr(self, r):
                return True

        return False
