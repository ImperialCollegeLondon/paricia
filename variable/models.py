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
from django.urls import reverse

from management.models import PermissionsBase
from sensor.models import Sensor
from station.models import Station


class Unit(PermissionsBase):
    """Unit of measurement with a name and a symbol.

    Attributes:
        unit_id (AutoField): Primary key.
        name (CharField): Name of the unit, eg. meters per second.
        initials (CharField): Symbol for the unit, eg. m/s.
    """

    unit_id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    name = models.CharField(
        "Name", max_length=50, help_text="Name of the unit, eg. meters per second."
    )
    initials = models.CharField(
        "Symbol", max_length=10, help_text="Symbol for the unit, eg. m/s."
    )

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return str(self.initials)

    def get_absolute_url(self) -> str:
        """Get the absolute URL of the object."""
        return reverse("variable:unit_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["unit_id"]


class Variable(PermissionsBase):
    """A variable with a physical meaning.

    Such as precipitation, wind speed, wind direction, soil moisture, including the
    associated unit. It also includes metadata to help identify what is a reasonable
    value for the data, to flag outliers and to help with the validation process.

    The nature of the variable can be one of the following:

    - sum: Cumulative value over a period of time.
    - average: Average value over a period of time.
    - value: One-off value.

    Attributes:
        variable_id (AutoField): Primary key.
        variable_code (CharField): Code of the variable, eg. airtemperature.
        name (CharField): Human-readable name of the variable, eg. Air temperature.
        unit (ForeignKey): Unit of the variable.
        maximum (DecimalField): Maximum value allowed for the variable.
        minimum (DecimalField): Minimum value allowed for the variable.
        diff_warning (DecimalField): If two sequential values in the time-series data of
            this variable differ by more than this value, the validation process can
            mark this with a warning flag.
        diff_error (DecimalField): If two sequential values in the time-series data of
            this variable differ by more than this value, the validation process can
            mark this with an error flag.
        outlier_limit (DecimalField): How many times the standard deviation (sigma) is
            considered an outlier for this variable.
        null_limit (DecimalField): The max % of null values (missing, caused by e.g.
            equipment malfunction) allowed for hourly, daily, monthly data. Cumulative
            values are not deemed trustworthy if the number of missing values in a given
            period is greater than the null_limit.
        nature (CharField): Nature of the variable, eg. if it represents a one-off
            value, the average over a period of time or the cumulative value over a
            period


    """

    NATURES = [("sum", "sum"), ("average", "average"), ("value", "value")]

    variable_id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    variable_code = models.CharField(
        "Code",
        max_length=100,
        help_text="Code of the variable, eg. airtemperature.",
    )
    name = models.CharField(
        "Name",
        max_length=50,
        help_text="Human-readable name of the variable, eg. Air temperature.",
    )
    unit = models.ForeignKey(
        Unit,
        models.PROTECT,
        blank=True,
        null=True,
        verbose_name="Unit",
        help_text="Unit of the variable.",
    )
    maximum = models.DecimalField(
        "Maximum",
        max_digits=7,
        decimal_places=2,
        help_text="Maximum value allowed for the variable.",
    )
    minimum = models.DecimalField(
        "Minimum",
        max_digits=7,
        decimal_places=2,
        help_text="Minimum value allowed for the variable.",
    )
    diff_warning = models.DecimalField(
        "Difference warning",
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="If two sequential values in the time-series data of this variable "
        "differ by more than this value, the validation process can mark this with a "
        "warning flag.",
        validators=[MinValueValidator(0)],
    )
    diff_error = models.DecimalField(
        "Difference error",
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="If two sequential values in the time-series data of this variable "
        "differ by more than this value, the validation process can mark this with an "
        "error flag.",
        validators=[MinValueValidator(0)],
    )
    outlier_limit = models.DecimalField(
        "Sigmas (outliers)",
        max_digits=7,
        decimal_places=2,
        null=True,
        blank=True,
        help_text="How many times the standard deviation (sigma) is considered an "
        "outlier for this variable.",
        validators=[MinValueValidator(0)],
    )
    null_limit = models.DecimalField(
        "Null limit (%)",
        max_digits=4,
        decimal_places=1,
        default=0,
        help_text="The max \\% of null values (missing, caused by e.g. equipment "
        "malfunction) allowed for hourly, daily, monthly data. Cumulative values are "
        "not deemed trustworthy if the number of missing values in a given "
        "period is greater than the null_limit.",
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    nature = models.CharField(
        "Nature of the measurement",
        max_length=10,
        choices=NATURES,
        default="value",
        help_text="Nature of the variable, eg. if it represents a one-off magnitude, "
        "the average over a period of time or the cumulative value over a period of "
        "time.",
    )

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Get the absolute URL of the object."""
        return reverse("variable:variable_detail", kwargs={"pk": self.pk})

    def clean(self) -> None:
        """Validate the model fields."""
        if self.maximum < self.minimum:
            raise ValidationError(
                {
                    "maximum": "The maximum value must be greater than the minimum "
                    "value."
                }
            )
        if self.diff_warning is not None and self.diff_error is not None:
            if self.diff_warning > self.diff_error:
                raise ValidationError(
                    {
                        "diff_warning": "The warning difference must be less than the "
                        "error difference."
                    }
                )
        if not self.variable_code.isidentifier():
            raise ValidationError(
                {
                    "variable_code": "The variable code must be a valid Python "
                    "identifier. Only letters, numbers and underscores are allowed, and"
                    " it cannot start with a number."
                }
            )
        return super().clean()

    @property
    def is_cumulative(self) -> bool:
        """Return True if the nature of the variable is sum."""
        return self.nature == "sum"

    class Meta:
        ordering = ["variable_id"]


class SensorInstallation(PermissionsBase):
    """Represents an installation of a Sensor at a Station, which measures a Variable.

    It includes metadata for installation and finishing date, as well as state (active
    or not).

    Attributes:
        sensorinstallation_id (AutoField): Primary key.
        variable (ForeignKey): Variable measured by the sensor.
        station (ForeignKey): Station where the sensor is installed.
        sensor (ForeignKey): Sensor used for the measurement.
        start_date (DateField): Start date of the installation.
        end_date (DateField): End date of the installation.
        state (BooleanField): Is the sensor active?
    """

    sensorinstallation_id = models.AutoField(
        "Id", primary_key=True, help_text="Primary key."
    )
    variable = models.ForeignKey(
        Variable,
        models.PROTECT,
        verbose_name="Variable",
        help_text="Variable measured by the sensor.",
    )
    station = models.ForeignKey(
        Station,
        models.PROTECT,
        verbose_name="Station",
        help_text="Station where the sensor is installed.",
    )
    sensor = models.ForeignKey(
        Sensor,
        models.PROTECT,
        verbose_name="Sensor",
        help_text="Sensor used for the measurement.",
    )
    start_date = models.DateField(
        "Start date", help_text="Start date of the installation"
    )
    end_date = models.DateField(
        "End date", blank=True, null=True, help_text="End date of the installation"
    )
    state = models.BooleanField(
        "Is active?", default=True, help_text="Is the sensor active?"
    )

    def get_absolute_url(self) -> str:
        """Get the absolute URL of the object."""
        return reverse("variable:sensorinstallation_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["station"]
