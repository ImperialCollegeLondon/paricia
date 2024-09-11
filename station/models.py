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
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.urls import reverse
from guardian.shortcuts import assign_perm, get_anonymous_user, remove_perm

from management.models import PermissionsBase

from .countries import COUNTRIES
from .timezones import TIMEZONES

# Global variables used in Basin model
BASIN_IMAGE_PATH = "station/basin_image/"
BASIN_FILE_PATH = "station/basin_file/"
PLACE_IMAGE_PATH = "station/place_image/"

User = get_user_model()


class Country(PermissionsBase):
    """The country where a station or region is in.

    Attributes:
        id (int): Primary key.
        name (str): Country name."""

    id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    name = models.CharField(
        max_length=100, choices=COUNTRIES, help_text="Country name."
    )

    def __str__(self) -> str:
        """Return the country name."""
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Return the absolute url of the country."""
        return reverse("station:country_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)
        verbose_name_plural = "countries"


class Region(PermissionsBase):
    """A region within a country.

    Attributes:
        id (int): Primary key.
        name (str): Name of the region.
        country (Country): Country where the region is located.
    """

    id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    name = models.CharField(
        max_length=32, verbose_name="Name", help_text="Name of the region."
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Country",
        help_text="Country where the region is located. In case of a region that is not"
        "spans multiple countries, select one of them or leave this field empty.",
    )

    def __str__(self) -> str:
        """Return the region name."""
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Return the absolute url of the region."""
        return reverse("station:region_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Ecosystem(PermissionsBase):
    """The ecosystem associated with a station.

    Attributes:
        id (int): Primary key.
        name (str): Name of the ecosystem, e.g. rain forest.
    """

    id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    name = models.CharField(
        max_length=32, help_text="Name of the ecosystem, eg. rain forest."
    )

    def __str__(self) -> str:
        """Return the ecosystem name."""
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Return the absolute url of the ecosystem."""
        return reverse("station:ecosystem_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Institution(PermissionsBase):
    """Institutional partner responsible for a station.

    Attributes:
        id (int): Primary key.
        name (str): Name of the institution.
    """

    id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    name = models.CharField(max_length=32, help_text="Name of the institution.")

    def __str__(self) -> str:
        """Return the institution name."""
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Return the absolute url of the institution."""
        return reverse("station:institution_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class StationType(PermissionsBase):
    """Type of the station, indicating what it measures.

    Attributes:
        id (int): Primary key.
        name (str): Name of the station type, e.g. pluvometric, hydrological.
    """

    id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    name = models.CharField(
        max_length=40,
        help_text="Name of the station type, eg. pluvometric, hydrological.",
    )

    def __str__(self) -> str:
        """Return the station type name."""
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Return the absolute url of the station type."""
        return reverse("station:station_type_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Place(PermissionsBase):
    """Specific place that a station is situated.

    Attributes:
        id (int): Primary key.
        name (str): Name of the place, e.g. Huaraz.
        image (FileField): Photography/Map of the location.
    """

    id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    name = models.CharField(max_length=40, help_text="Name of the place, eg. Huaraz.")
    image = models.ImageField(
        "Photography/Map",
        upload_to=PLACE_IMAGE_PATH,
        null=True,
        blank=True,
        help_text="Photography/Map of the location.",
    )

    def __str__(self) -> str:
        """Return the place name."""
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Return the absolute url of the place."""
        return reverse("station:place_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Basin(PermissionsBase):
    """Basin e.g. El Carmen.
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


class PlaceBasin(PermissionsBase):
    """Associates a Basin with a Place and an image."""

    id = models.AutoField("Id", primary_key=True)
    place = models.ForeignKey(
        Place, on_delete=models.PROTECT, null=True, verbose_name="Place"
    )
    basin = models.ForeignKey(
        Basin, on_delete=models.PROTECT, null=True, verbose_name="Basin"
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


class Station(PermissionsBase):
    """Main representation of a station with lots of metadata, according to
    the other models in this app, along with some geographical data.
    """

    VISIBILITY_LEVELS = [
        ("public", "Public"),
        ("internal", "Internal"),
        ("private", "Private"),
    ]

    visibility = models.CharField(
        max_length=8, choices=VISIBILITY_LEVELS, default="private"
    )

    station_id = models.AutoField("Id", primary_key=True)
    station_code = models.CharField("Code", max_length=32)
    station_name = models.CharField(
        "Description", max_length=100, null=True, blank=True
    )
    station_type = models.ForeignKey(
        StationType,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="StationType",
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Country",
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Region/Province/Department",
    )
    ecosystem = models.ForeignKey(
        Ecosystem,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Ecosystem",
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Institution",
    )
    place_basin = models.ForeignKey(
        PlaceBasin,
        on_delete=models.PROTECT,
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
    timezone = models.CharField("Timezone", max_length=100, choices=TIMEZONES)

    def __str__(self):
        return str(self.station_code)

    def get_absolute_url(self):
        return reverse("station:station_detail", kwargs={"pk": self.pk})

    def set_object_permissions(self):
        """Set object-level permissions."""
        super().set_object_permissions()

        standard_group = Group.objects.get(name="Standard")
        anonymous_user = get_anonymous_user()

        # Assign view_measurements permission based on permissions level
        if self.visibility == "public":
            assign_perm("view_measurements", standard_group, self)
            assign_perm("view_measurements", anonymous_user, self)
            if self.owner:
                remove_perm("view_measurements", self.owner, self)
        elif self.visibility == "internal":
            assign_perm("view_measurements", standard_group, self)
            remove_perm("view_measurements", anonymous_user, self)
            if self.owner:
                remove_perm("view_measurements", self.owner, self)
        elif self.visibility == "private":
            remove_perm("view_measurements", standard_group, self)
            remove_perm("view_measurements", anonymous_user, self)
            if self.owner:
                assign_perm("view_measurements", self.owner, self)

    class Meta:
        ordering = ("station_id",)
        permissions = (("view_measurements", "View measurements"),)


# TODO Discuss if it's necessary to implement multiple deltaTs for different dates
class DeltaT(PermissionsBase):
    """Delta T: Interval of data adquisition (In minutes)"""

    id = models.AutoField("Id", primary_key=True)
    station = models.ForeignKey(
        Station,
        on_delete=models.CASCADE,
        verbose_name="Station",
    )
    delta_t = models.PositiveSmallIntegerField()

    def __str__(self):
        return str(self.station.station_code + " - " + str(self.delta_t))

    def get_absolute_url(self):
        return reverse("station:delta_t_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)
