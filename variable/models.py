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
from sensor.models import Sensor
from station.models import Station


class Unit(PermissionsBase):
    """Unit of measurement with a name and an initialised form.

    For example, e.g. metres per second, m/s.
    """

    unit_id = models.AutoField("Id", primary_key=True)
    name = models.CharField("Name", max_length=50)
    initials = models.CharField("Initials", max_length=10)

    def __str__(self):
        return str(self.initials)

    def get_absolute_url(self):
        return reverse("variable:unit_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["unit_id"]


class Variable(PermissionsBase):
    """A variable e.g. precipitation, wind speed, wind direction, soil moisture,
    with an associated unit.
    The variable_code must match the name of one of the classes in measurement.models.
    There are max and min allowed values as well as:
    diff_warning: If two sequential values in the time-series data of this variable
        differ by more than this value, the validation process can mark this with a
        warning flag.
    diff_error: If two sequential values in the time-series data of this variable
        differ by more than this value, the validation process can mark this with an
        error flag.
    is_active: True if the variable is in use in the database.
    is_cumulative: True if the variable is accumulated over time, False if it is
        averaged over time.
    outlier_limit: How many times the standard deviation (sigma) is considered an
        outlier for this variable.
    automatic_report: True if this variable should be included in automatic hourly,
        daily etc. reporting scripts.
    null_limit: The max % of null (missing, Caused by e.g. equipment malfunction) values
        allowed for hourly, daily, monthly data. Cumulative values are not deemed
        trustworthy if the number of missing values in a given period > null_limit.
    """

    NATURES = [("sum", "sum"), ("average", "average"), ("value", "value")]

    variable_id = models.AutoField("Id", primary_key=True)
    variable_code = models.CharField("Code", max_length=100)
    name = models.CharField("Name", max_length=50)
    unit = models.ForeignKey(
        Unit, models.SET_NULL, blank=True, null=True, verbose_name="Unit"
    )
    maximum = models.DecimalField("Maximum", max_digits=7, decimal_places=2)
    minimum = models.DecimalField("Minimum", max_digits=7, decimal_places=2)
    diff_warning = models.DecimalField(
        "Difference warning", max_digits=7, decimal_places=2, null=True, blank=True
    )
    diff_error = models.DecimalField(
        "Difference error", max_digits=7, decimal_places=2, null=True, blank=True
    )
    outlier_limit = models.DecimalField(
        "Sigmas (outliers)", max_digits=7, decimal_places=2, null=True, blank=True
    )
    is_active = models.BooleanField("Active", default=True)
    automatic_report = models.BooleanField("Automatic report", default=True)
    null_limit = models.DecimalField(
        "Null limit (%)", max_digits=4, decimal_places=1, null=True
    )
    nature = models.CharField("Nature", max_length=10, choices=NATURES, default="value")

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("variable:variable_detail", kwargs={"pk": self.pk})

    @property
    def is_cumulative(self) -> bool:
        return self.nature == "sum"

    class Meta:
        ordering = ["variable_id"]


class SensorInstallation(PermissionsBase):
    """Represents an installation of a Sensor at a Station, which measures a Variable.
    Metadata for installation and finishing date, as well as state (active or not).
    """

    sensorinstallation_id = models.AutoField("Id", primary_key=True)
    variable = models.ForeignKey(
        Variable, models.SET_NULL, blank=True, null=True, verbose_name="Variable"
    )
    station = models.ForeignKey(
        Station, models.SET_NULL, blank=True, null=True, verbose_name="Station"
    )
    sensor = models.ForeignKey(
        Sensor, models.SET_NULL, blank=True, null=True, verbose_name="Sensor"
    )
    start_date = models.DateField("Start date")
    end_date = models.DateField("End date", blank=True, null=True)
    state = models.BooleanField("Active", default=True)

    def get_absolute_url(self):
        return reverse("variable:sensorinstallation_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["station"]
