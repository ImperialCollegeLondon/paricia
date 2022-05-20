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
from station.models import Station

from variable.models import Variable


class Extension(models.Model):
    """
    File extension.
    """

    extension_id = models.AutoField("Id", primary_key=True)
    value = models.CharField("Value", max_length=5)

    def __str__(self):
        return str(self.ext_valor)

    def get_absolute_url(self):
        return reverse("format:extension_index")


class Delimiter(models.Model):
    """
    Data delimiter
    """

    delimiter_id = models.AutoField("Id", primary_key=True)
    name = models.CharField("Name", max_length=100)
    character = models.CharField("Character", max_length=10, blank=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("format:delimiter_index")


class Date(models.Model):
    """
    Date format
    """

    date_id = models.AutoField("Id", primary_key=True)
    format = models.CharField("Format", max_length=20)
    code = models.CharField("Code", max_length=20)

    def __str__(self):
        return str(self.fec_format)

    def get_absolute_url(self):
        return reverse("format:date_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("date_id",)


class Time(models.Model):
    """
    Time format
    """

    time_id = models.AutoField("Id", primary_key=True)
    format = models.CharField("Format", max_length=20)
    code = models.CharField("Code", max_length=20)

    def __str__(self):
        return str(self.hor_format)

    def get_absolute_url(self):
        return reverse("format:time_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("time_id",)


class Format(models.Model):
    """
    Details of the data file format, combining different aspects.
    """

    format_id = models.AutoField("format_id", primary_key=True)
    extension = models.ForeignKey(
        Extension,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="File extension",
    )
    delimiter = models.ForeignKey(
        Delimiter,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Delimiter",
    )
    name = models.CharField("Format name", max_length=35)
    description = models.TextField("Description", null=True)
    location = models.CharField("Location", max_length=300, blank=True, null=True)
    file = models.CharField(
        "Archivo",
        max_length=100,
        blank=True,
        null=True,
        help_text="Only applies to automatic transmission",
    )
    first_row = models.SmallIntegerField("First row")
    last_row = models.SmallIntegerField("Last row", blank=True, null=True)
    date = models.ForeignKey(
        Date,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Date format",
    )
    utc_date = models.BooleanField("Is time UTC? (substract 5 hours)", default=False)
    date_column = models.SmallIntegerField("Date column")
    time = models.ForeignKey(
        Time,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Time format",
    )
    time_column = models.SmallIntegerField("Time column")
    format_type = models.CharField(
        "Tipo de Formato",
        max_length=25,
        choices=(
            ("automatic", "automatic"),
            ("conventional", "conventional"),
        ),
    )
    status = models.BooleanField("Status", default=True)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("format:format_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("-for_id",)


class Clasification(models.Model):
    """
    Classification details.
    """

    cls_id = models.AutoField("Id", primary_key=True)
    format = models.ForeignKey(Format, on_delete=models.CASCADE, verbose_name="Format")
    variable = models.ForeignKey(
        Variable, on_delete=models.CASCADE, verbose_name="Variable"
    )
    value = models.SmallIntegerField("Value column")
    maximum = models.SmallIntegerField("Maximum value column", blank=True, null=True)
    minimum = models.SmallIntegerField("Minimum value column", blank=True, null=True)
    value_validator_column = models.SmallIntegerField(
        "Value validator column", blank=True, null=True
    )
    value_validator_text = models.CharField(
        "Value validator text", max_length=10, blank=True, null=True
    )
    maximum_validator_column = models.SmallIntegerField(
        "Maximum value validator column", blank=True, null=True
    )
    maximum_validator_text = models.CharField(
        "Maximum value  validator text", max_length=10, blank=True, null=True
    )
    minimum_validator_column = models.SmallIntegerField(
        "Minimum value validator column", blank=True, null=True
    )
    minimum_validator_text = models.CharField(
        "Minimum value validator text", max_length=10, blank=True, null=True
    )
    accumulate = models.BooleanField("Accumulate every 5 min?", default=False)
    incremental = models.BooleanField("Is it an incremental counter?", default=False)
    resolution = models.DecimalField(
        "Resolution", max_digits=6, decimal_places=2, blank=True, null=True
    )
    decimal_comma = models.BooleanField(
        "Uses comma as decimal separator?", default=False
    )

    def __str__(self):
        return str(self.cla_id)

    def get_absolute_url(self):
        return reverse("format:clasificacion_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("var_id",)


class Association(models.Model):
    """
    Associates a data format with a station.
    """

    association_id = models.AutoField("Id", primary_key=True)
    format = models.ForeignKey(
        Format, models.SET_NULL, blank=True, null=True, verbose_name="Format"
    )
    station = models.ForeignKey(
        Station, models.SET_NULL, blank=True, null=True, verbose_name="Station"
    )

    def get_absolute_url(self):
        return reverse("format:association_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("aso_id",)
        unique_together = (
            "station",
            "format",
        )
