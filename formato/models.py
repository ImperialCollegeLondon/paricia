# -*- coding: utf-8 -*-

################################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos (iMHEA)
# basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#         Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS), Ecuador.
#         Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones creadoras,
#              ya sea en uso total o parcial del código.

from __future__ import unicode_literals

from django.db import models
from django.urls import reverse

from estacion.models import Estacion
from variable.models import Variable


class Extension(models.Model):
    """The file extension associated with the Format.
    GENERALISE: Could be replaced with simpler MIME type checks.
    """

    ext_id = models.AutoField("Id", primary_key=True)
    ext_valor = models.CharField("Valor", max_length=5)

    def __str__(self):
        return str(self.ext_valor)

    def get_absolute_url(self):
        return reverse("formato:extension_index")


class Delimitador(models.Model):
    """Delimiter associated with the Format.
    GENERALISE: Probably doesn't need to be its own model, could be simplified.
    """

    del_id = models.AutoField("Id", primary_key=True)
    del_nombre = models.CharField("Nombre", max_length=100)
    del_caracter = models.CharField("Caracter", max_length=10, blank=True)

    def __str__(self):
        return str(self.del_nombre)

    def get_absolute_url(self):
        return reverse("formato:delimitador_index")


class Fecha(models.Model):
    """Date format associated with the Format, e.g. MM/DD/YYYY, DD.MM.YYYY etc.
    GENERALISE: similar to above.
    """

    fec_id = models.AutoField("Id", primary_key=True)
    fec_formato = models.CharField("Formato", max_length=20)
    fec_codigo = models.CharField("Código", max_length=20)

    def __str__(self):
        return str(self.fec_formato)

    def get_absolute_url(self):
        return reverse("formato:fecha_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("fec_id",)


class Hora(models.Model):
    """Time format associated with the Format, e.g. HH/MM/SS 24H etc.
    GENERALISE: similar to above.
    """

    hor_id = models.AutoField("Id", primary_key=True)
    hor_formato = models.CharField("Formato", max_length=20)
    hor_codigo = models.CharField("Código", max_length=20)

    def __str__(self):
        return str(self.hor_formato)

    def get_absolute_url(self):
        return reverse("formato:hora_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("hor_id",)


class Formato(models.Model):
    """Defines a format (of a file, time-series data) in terms of its extension,
    first data row etc. Used when importing data files in importacion.functions.
    GENERALISE: Some of the FK models (date format etc.) may be simple charfield etc.
    NEWNAME: Format
    """

    for_id = models.AutoField("for_id", primary_key=True)
    ext_id = models.ForeignKey(
        Extension,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Extensión del Archivo",
    )
    del_id = models.ForeignKey(
        Delimitador,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Delimitador",
    )
    for_nombre = models.CharField("Nombre del Formato", max_length=35)
    for_descripcion = models.TextField("Descripción", null=True)
    for_ubicacion = models.CharField("Ubicación", max_length=300, blank=True, null=True)
    for_archivo = models.CharField(
        "Archivo",
        max_length=100,
        blank=True,
        null=True,
        help_text="Solo aplica para transmisión automática",
    )
    for_fil_ini = models.SmallIntegerField("Fila de inicio")
    for_fil_cola = models.SmallIntegerField(
        "Número de filas de cola", blank=True, null=True
    )
    fec_id = models.ForeignKey(
        Fecha,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Formato de Fecha",
    )
    es_fecha_utc = models.BooleanField("¿Es fecha UTC? (Resta 5 horas)", default=False)
    for_col_fecha = models.SmallIntegerField("Columna fecha")
    hor_id = models.ForeignKey(
        Hora,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name="Formato de Hora",
    )
    for_col_hora = models.SmallIntegerField("Columna de hora")
    for_tipo = models.CharField(
        "Tipo de Formato",
        max_length=25,
        choices=(
            ("automatico", "automático"),
            ("convencional", "convencional"),
        ),
    )
    for_estado = models.BooleanField("Estado", default=True)

    def __str__(self):
        return str(self.for_nombre)

    def get_absolute_url(self):
        return reverse("formato:formato_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("-for_id",)


class Clasificacion(models.Model):
    """Classification linking Format and Variable with metadata for column value,
    column value max/min etc. Used in import app to check if data already exists
    for a certain date range-Station-Value cobination and in some other function.
    HELPWANTED: Unclear exactly what this is doing, seems quite abstract.
        --> DIEGO: Question for Pablo
    """

    cla_id = models.AutoField("Id", primary_key=True)
    for_id = models.ForeignKey(
        Formato, on_delete=models.CASCADE, verbose_name="Formato"
    )
    var_id = models.ForeignKey(
        Variable, on_delete=models.CASCADE, verbose_name="Variable"
    )
    cla_valor = models.SmallIntegerField("Columna valor")
    cla_maximo = models.SmallIntegerField("Columna valor máximo", blank=True, null=True)
    cla_minimo = models.SmallIntegerField("Columna valor mínimo", blank=True, null=True)
    col_validador_valor = models.SmallIntegerField(
        "Columna validador Valor", blank=True, null=True
    )
    txt_validador_valor = models.CharField(
        "Texto validador Valor", max_length=10, blank=True, null=True
    )
    col_validador_maximo = models.SmallIntegerField(
        "Columna validador Máximo", blank=True, null=True
    )
    txt_validador_maximo = models.CharField(
        "Texto validador Máximo", max_length=10, blank=True, null=True
    )
    col_validador_minimo = models.SmallIntegerField(
        "Columna validador Mínimo", blank=True, null=True
    )
    txt_validador_minimo = models.CharField(
        "Texto validador Mínimo", max_length=10, blank=True, null=True
    )
    acumular = models.BooleanField("¿Acumular a 5 minutos?", default=False)
    incremental = models.BooleanField("¿Es contador incremental?", default=False)
    resolucion = models.DecimalField(
        "Resolución", max_digits=6, decimal_places=2, blank=True, null=True
    )
    coma_decimal = models.BooleanField("COMA: separador decimal", default=False)

    def __str__(self):
        return str(self.cla_id)

    def get_absolute_url(self):
        return reverse("formato:clasificacion_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("var_id",)


class Asociacion(models.Model):
    """Associates a Format with a Station. Used to return a list of formats associated
    with a station.
    HELPWANTED: Unclear what the use case for this is. --> DIEGO: Question for Pablo
    """

    aso_id = models.AutoField("Id", primary_key=True)
    for_id = models.ForeignKey(
        Formato, models.SET_NULL, blank=True, null=True, verbose_name="Formato"
    )
    est_id = models.ForeignKey(
        Estacion, models.SET_NULL, blank=True, null=True, verbose_name="Estación"
    )

    def get_absolute_url(self):
        return reverse("formato:asociacion_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("aso_id",)
        unique_together = (
            "est_id",
            "for_id",
        )
