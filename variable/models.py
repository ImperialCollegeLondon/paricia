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

from django.db import models
from django.urls import reverse

from sensor.models import Sensor
from station.models import Station


class Unit(models.Model):
    """
    Unit of measurement with a name and an initialised form e.g. metres per second, m/s.
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


class Variable(models.Model):
    """
    A variable e.g. precipitation, wind speed, wind direction, soil moisture,
    with an associated unit. Also has max, min... TODO: finish.
    """

    variable_id = models.AutoField("Id", primary_key=True)
    variable_code = models.CharField("Code", max_length=7)
    name = models.CharField("Name", max_length=50)
    unit_id = models.ForeignKey(
        Unit, models.SET_NULL, blank=True, null=True, verbose_name="Unidad"
    )
    maximum = models.DecimalField("Maximum", max_digits=7, decimal_places=2)
    minimum = models.DecimalField("Minimum", max_digits=7, decimal_places=2)
    # TODO translate var_sos, var_err, var_estado and vacios if they're needed
    # otherwise delete
    var_sos = models.DecimalField(
        "Incremento sospechoso", max_digits=7, decimal_places=2, null=True, blank=True
    )
    var_err = models.DecimalField(
        "Incremento error", max_digits=7, decimal_places=2, null=True, blank=True
    )
    var_min = models.DecimalField(
        "Sigmas (outliers)", max_digits=7, decimal_places=2, null=True, blank=True
    )
    var_estado = models.BooleanField("Estado", default=True)
    is_cumulative = models.BooleanField(
        "Cumulative (True) or Averaged (False)", default=True
    )
    automatic_report = models.BooleanField("Automatic report", default=True)
    vacios = models.DecimalField(
        "Vacíos (%)", max_digits=4, decimal_places=1, null=True
    )

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("variable:variable_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ["variable_id"]


class SensorInstallation(models.Model):
    """
    Represents an installation of a Sensor at a Station, which measures a Variable.
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
