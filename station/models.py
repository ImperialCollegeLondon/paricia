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

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse

# Global variables used in Basin model
BASIN_IMAGE_PATH = "station/basin_image/"
BASIN_FILE_PATH = "station/basin_file/"


class Country(models.Model):
    """
    The country that a station or region is in.
    """

    id = models.AutoField("Id", primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("station:country_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Region(models.Model):
    """
    A region within a country.
    """

    id = models.AutoField("Id", primary_key=True)
    name = models.CharField(max_length=32, verbose_name="Name")
    country = models.ForeignKey(
        Country, on_delete=models.SET_NULL, null=True, verbose_name="Country"
    )

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("station:region_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Ecosystem(models.Model):
    """
    The ecosystem associated with a station e.g. rain forest.
    """

    id = models.AutoField("Id", primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("station:ecosystem_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Institution(models.Model):
    """
    Institutional partner e.g. Imperial College London.
    """

    id = models.AutoField("Id", primary_key=True)
    name = models.CharField(max_length=32)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("station:institution_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class StationType(models.Model):
    """
    Station type e.g. pluvometric, hydrological.
    """

    id = models.AutoField("Id", primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("station:station_type_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Place(models.Model):
    """
    Specific place that a station is situated e.g. Huaraz.
    """

    id = models.AutoField("Id", primary_key=True)
    name = models.CharField(max_length=40)
    image = models.FileField(
        "Photography/Map", upload_to="station/place_image/", null=True, blank=True
    )

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("station:place_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Basin(models.Model):
    """
    Basin e.g. El Carmen.
    TODO: Is there a more specific definition we can use? e.g. a river basin?
    """

    id = models.AutoField("Id", primary_key=True)
    name = models.CharField(max_length=40)
    image = models.FileField(
        "Photography/Map", upload_to=BASIN_IMAGE_PATH, null=True, blank=True
    )
    file = models.FileField(
        "File(PDF)", upload_to=BASIN_FILE_PATH, null=True, blank=True
    )

    def __str__(self):
        return str(self.name)

    def get_absolute_url(self):
        return reverse("station:basin_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class PlaceBasin(models.Model):
    """
    Associates a Basin with a Place and an image.
    """

    id = models.AutoField("Id", primary_key=True)
    place = models.ForeignKey(
        Place, on_delete=models.SET_NULL, null=True, verbose_name="Place"
    )
    basin = models.ForeignKey(
        Basin, on_delete=models.SET_NULL, null=True, verbose_name="Basin"
    )
    image = models.FileField(
        "Photography/Map",
        upload_to="station/place_basin_image/",
        null=True,
        blank=True,
    )

    def __str__(self):
        return str(self.place) + " - " + str(self.basin)

    def get_absolute_url(self):
        return reverse("station:place_basin_detail", kwargs={"pk": self.pk})

    class Meta:
        unique_together = ("place", "basin")
        ordering = ("id",)


class Station(models.Model):
    """
    Main representation of a station with lots of metadata, according to
    the other models in this app, along with some geographical data.
    """

    station_id = models.AutoField("Id", primary_key=True)
    station_code = models.CharField("Code", max_length=32)
    station_name = models.CharField(
        "Description", max_length=100, null=True, blank=True
    )
    station_type = models.ForeignKey(
        StationType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="StationType",
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Country",
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Region/Province/Department",
    )
    ecosystem = models.ForeignKey(
        Ecosystem,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Ecosystem",
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Institution",
    )
    place_basin = models.ForeignKey(
        PlaceBasin,
        on_delete=models.SET_NULL,
        verbose_name="Place-Basin",
        null=True,
        blank=True,
    )
    station_state = models.BooleanField("Operational", default=True)
    station_latitude = models.DecimalField(
        "Latitude", max_digits=17, decimal_places=14, null=True, blank=True
    )
    station_longitude = models.DecimalField(
        "Longitude", max_digits=17, decimal_places=14, null=True, blank=True
    )
    station_altitude = models.IntegerField(
        "Altitude",
        null=True,
        blank=True,
        validators=[MaxValueValidator(6000), MinValueValidator(0)],
    )
    station_file = models.FileField(
        "Photography/File",
        upload_to="station/station_file/",
        null=True,
        blank=True,
    )
    station_external = models.BooleanField("External", default=False)
    influence_km = models.DecimalField(
        "Área of input (km)", max_digits=12, decimal_places=4, null=True, blank=True
    )

    def __str__(self):
        return str(self.station_code)

    def get_absolute_url(self):
        return reverse("station:station_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("station_id",)


# TODO Discuss if it's really necessary to implement multiple deltaTs for different dates
class DeltaT(models.Model):
    """
    Delta T: Interval of data adquisition (In minutes)
    """
    id = models.AutoField("Id", primary_key=True)
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        verbose_name="Station",
    )
    delta_t = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.station.station_code + ' - ' + str(self.delta_t))

    def get_absolute_url(self):
        return reverse("station:delta_t_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)