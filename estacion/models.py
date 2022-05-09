# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

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

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse


class Pais(models.Model):
    """The country that a station, region etc. is in.
    NEWNAME: Country
    """

    id = models.AutoField("Id", primary_key=True)
    nombre = models.CharField(max_length=32)

    def __str__(self):
        return str(self.nombre)

    def get_absolute_url(self):
        return reverse("estacion:pais_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Region(models.Model):
    """A Region that is within a country."""

    id = models.AutoField("Id", primary_key=True)
    nombre = models.CharField(max_length=32, verbose_name="Nombre")
    pais = models.ForeignKey(
        Pais, on_delete=models.SET_NULL, null=True, verbose_name="País"
    )

    def __str__(self):
        return str(self.nombre)

    def get_absolute_url(self):
        return reverse("estacion:region_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Ecosistema(models.Model):
    """The ecosystem associated with a station.
    NEWNAME: Ecosystem
    """

    id = models.AutoField("Id", primary_key=True)
    nombre = models.CharField(max_length=32)

    def __str__(self):
        return str(self.nombre)

    def get_absolute_url(self):
        return reverse("estacion:ecosistema_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Socio(models.Model):
    """Partner associated with the station e.g. FONAG, Imperial College London.
    NEWNAME: Partner/Institution
    """

    id = models.AutoField("Id", primary_key=True)
    nombre = models.CharField(max_length=32)

    def __str__(self):
        return str(self.nombre)

    def get_absolute_url(self):
        return reverse("estacion:socio_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Tipo(models.Model):
    """Type of station e.g. pluviometric, hydrometric.
    NEWNAME: StationType
    """

    id = models.AutoField("Id", primary_key=True)
    nombre = models.CharField(max_length=40)

    def __str__(self):
        return str(self.nombre)

    def get_absolute_url(self):
        return reverse("estacion:tipo_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Sitio(models.Model):
    """Site associated with a SiteBasin.
    NEWNAME: Site
    """

    id = models.AutoField("Id", primary_key=True)
    nombre = models.CharField(max_length=40)
    imagen = models.FileField(
        "Fotografía/Mapa", upload_to="estacion/sitio_imagen/", null=True, blank=True
    )

    def __str__(self):
        return str(self.nombre)

    def get_absolute_url(self):
        return reverse("estacion:sitio_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


CUENCA_IMAGEN_PATH = "estacion/cuenca_imagen/"
CUENCA_FICHA_PATH = "estacion/cuenca_ficha/"


class Cuenca(models.Model):
    """Basin associated with a site via SiteBasin.
    Has an image for an image/map of the basin, and a file.
    NEWNAME: Basin
    HELPWANTED: What is the file for if not an image? --> DIEGO: I think it is an image
    + some metadata in PDF form about the station. Not sure if that was your question.
    """

    id = models.AutoField("Id", primary_key=True)
    nombre = models.CharField(max_length=40)
    imagen = models.FileField(
        "Fotografía/Mapa", upload_to=CUENCA_IMAGEN_PATH, null=True, blank=True
    )
    ficha = models.FileField(
        "Ficha(PDF)", upload_to=CUENCA_FICHA_PATH, null=True, blank=True
    )

    def __str__(self):
        return str(self.nombre)

    def get_absolute_url(self):
        return reverse("estacion:cuenca_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class SitioCuenca(models.Model):
    """SiteBasin: A combination of one Site and one Basin, with another image file.
    NEWNAME: SiteBasin
    """

    id = models.AutoField("Id", primary_key=True)
    sitio = models.ForeignKey(
        Sitio, on_delete=models.SET_NULL, null=True, verbose_name="Sitio"
    )
    cuenca = models.ForeignKey(
        Cuenca, on_delete=models.SET_NULL, null=True, verbose_name="Cuenca"
    )
    imagen = models.FileField(
        "Fotografía/Mapa",
        upload_to="estacion/sitiocuenca_imagen/",
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.sitio) + " - " + str(self.cuenca)

    def get_absolute_url(self):
        return reverse("estacion:sitiocuenca_detail", kwargs={"pk": self.pk})

    class Meta:
        unique_together = ("sitio", "cuenca")
        ordering = ("id",)


class Estacion(models.Model):
    """Main representation of a station with lots of metadata, according to
    the other models in this app, along with some geographical data.
    NEWNAME: Station
    """

    est_id = models.AutoField("Id", primary_key=True)
    est_codigo = models.CharField("Código", max_length=32)
    est_nombre = models.CharField("Descripción", max_length=100, null=True, blank=True)
    tipo = models.ForeignKey(
        Tipo, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Tipo"
    )
    pais = models.ForeignKey(
        Pais, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="País"
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Región/Provincia/Departamento",
    )
    ecosistema = models.ForeignKey(
        Ecosistema,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ecosistema",
    )
    socio = models.ForeignKey(
        Socio, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Socio"
    )
    sitiocuenca = models.ForeignKey(
        SitioCuenca,
        on_delete=models.SET_NULL,
        verbose_name="Sitio-Cuenca",
        null=True,
        blank=True,
    )
    est_estado = models.BooleanField("Operativa", default=True)
    est_latitud = models.DecimalField(
        "Latitud", max_digits=17, decimal_places=14, null=True, blank=True
    )
    est_longitud = models.DecimalField(
        "Longitud", max_digits=17, decimal_places=14, null=True, blank=True
    )
    est_altura = models.IntegerField(
        "Altura",
        null=True,
        blank=True,
        validators=[MaxValueValidator(6000), MinValueValidator(0)],
    )
    est_ficha = models.FileField(
        "Fotografía/Archivo",
        upload_to="estacion/estacion_ficha/",
        null=True,
        blank=True,
    )
    est_externa = models.BooleanField("Externa", default=False)
    influencia_km = models.DecimalField(
        "Área de Aporte (km)", max_digits=12, decimal_places=4, null=True, blank=True
    )

    def __str__(self):
        return str(self.est_codigo)

    def get_absolute_url(self):
        return reverse("estacion:estacion_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("est_id",)
