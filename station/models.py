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
PLACE_BASIN_IMAGE_PATH = "station/place_basin_image/"
STATION_IMAGE_PATH = "station/station_image/"

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
        return reverse("station:stationtype_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class Place(PermissionsBase):
    """Specific place that a station is situated.

    Attributes:
        id (int): Primary key.
        name (str): Name of the place, e.g. Huaraz.
        image (ImageField): Photography/Map of the location.
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
    """River(s) basin where the station is located e.g. El Carmen.

    Attributes:
        id (int): Primary key.
        name (str): Name of the basin, e.g. El Carmen.
        image (ImageField): Photography/Map of the basin.
        file (FileField): PDF file with details of the basin.
    """

    id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    name = models.CharField(
        max_length=40, help_text="Name of the basin, eg. El Carmen."
    )
    image = models.ImageField(
        "Photography/Map",
        upload_to=BASIN_IMAGE_PATH,
        null=True,
        blank=True,
        help_text="Photography/Map of the basin.",
    )
    file = models.FileField(
        "File(PDF)",
        upload_to=BASIN_FILE_PATH,
        null=True,
        blank=True,
        help_text="PDF file with details of the basin.",
    )

    def __str__(self) -> str:
        """Return the basin name."""
        return str(self.name)

    def get_absolute_url(self) -> str:
        """Return the absolute url of the basin."""
        return reverse("station:basin_detail", kwargs={"pk": self.pk})

    class Meta:
        ordering = ("id",)


class PlaceBasin(PermissionsBase):
    """Associates a Basin with a Place and an image.

    Attributes:
        id (int): Primary key.
        place (Place): Place of the association.
        basin (Basin): Basin of the association.
        image (ImageField): Photography/Map of the place within the basin.
    """

    id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    place = models.ForeignKey(
        Place,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Place",
        help_text="Place of the association.",
    )
    basin = models.ForeignKey(
        Basin,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Basin",
        help_text="Basin of the association.",
    )
    image = models.ImageField(
        "Photography/Map",
        upload_to=PLACE_BASIN_IMAGE_PATH,
        null=True,
        blank=True,
        help_text="Photography/Map of the place within the basin.",
    )

    def __str__(self) -> str:
        """Return the place-basin association."""
        return str(self.place) + " - " + str(self.basin)

    def get_absolute_url(self) -> str:
        """Return the absolute url of the place-basin association."""
        return reverse("station:placebasin_detail", kwargs={"pk": self.pk})

    class Meta:
        unique_together = ("place", "basin")
        ordering = ("id",)


class Station(PermissionsBase):
    """Main representation of a station, including several metadata.

    Attributes:
        visibility (str): Visibility level of the object, including an "internal"
            option.
        station_id (int): Primary key.
        station_code (str): Unique code for the station.
        station_name (str): Brief description of the station.
        station_type (StationType): Type of the station.
        country (Country): Country where the station is located.
        region (Region): Region within the Country where the station is located.
        ecosystem (Ecosystem): Ecosystem associated with the station.
        institution (Institution): Institutional partner responsible for the station.
        place_basin (PlaceBasin): Place-Basin association.
        station_state (bool): Is the station operational?
        timezone (str): Timezone of the station.
        station_latitude (Decimal): Latitude of the station, in degrees [-90 to 90].
        station_longitude (Decimal): Longitude of the station, in degrees [-180 to 180].
        station_altitude (int): Altitude of the station.
        influence_km (Decimal): Area of influence in km2.
        station_file (ImageField): Photography of the station.
        station_external (bool): Is the station external?
        variables (str): Comma-separated list of variables measured by the station.
    """

    VISIBILITY_LEVELS = [
        ("public", "Public"),
        ("internal", "Internal"),
        ("private", "Private"),
    ]

    visibility = models.CharField(
        max_length=8,
        choices=VISIBILITY_LEVELS,
        default="private",
        help_text="Visibility level of the station, including an 'internal' option. "
        "WARNING: Changing this setting will affect the permissions of the object. If "
        "'Public', all users will be able to view and associate the object with their "
        "own. If 'Internal', only users with the 'Standard' group will be able to view"
        "the measurements associated with the station.",
    )

    station_id = models.AutoField("Id", primary_key=True, help_text="Primary key.")
    station_code = models.CharField(
        "Code", max_length=32, unique=True, help_text="Unique code for the station."
    )
    station_name = models.CharField(
        "Description",
        max_length=100,
        null=True,
        blank=True,
        help_text="Brief description of the station.",
    )
    station_type = models.ForeignKey(
        StationType,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Station type",
        help_text="Type of the station, indicating what it measures.",
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.PROTECT,
        verbose_name="Country",
        null=True,
        help_text="Country where the station is located.",
    )
    region = models.ForeignKey(
        Region,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Region",
        help_text="Region within the Country where the station is located.",
    )
    ecosystem = models.ForeignKey(
        Ecosystem,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name="Ecosystem",
        help_text="Ecosystem associated with the station.",
    )
    institution = models.ForeignKey(
        Institution,
        on_delete=models.PROTECT,
        null=True,
        verbose_name="Institution",
        help_text="Institutional partner responsible for the station.",
    )
    place_basin = models.ForeignKey(
        PlaceBasin,
        on_delete=models.PROTECT,
        verbose_name="Place-Basin",
        null=True,
        blank=True,
        help_text="Place-Basin association.",
    )
    station_state = models.BooleanField(
        "Operational", default=True, help_text="Is the station operational?"
    )
    timezone = models.CharField(
        "Timezone",
        max_length=100,
        choices=TIMEZONES,
        help_text="Timezone of the station.",
    )
    station_latitude = models.DecimalField(
        "Latitude",
        max_digits=17,
        decimal_places=14,
        null=True,
        blank=True,
        help_text="Latitude of the station, in degrees [-90 to 90].",
        validators=[MaxValueValidator(90), MinValueValidator(-90)],
    )
    station_longitude = models.DecimalField(
        "Longitude",
        max_digits=17,
        decimal_places=14,
        null=True,
        blank=True,
        help_text="Longitude of the station, in degrees [-180 to 180].",
        validators=[MaxValueValidator(180), MinValueValidator(-180)],
    )
    station_altitude = models.IntegerField(
        "Altitude",
        null=True,
        blank=True,
        validators=[MaxValueValidator(6000), MinValueValidator(0)],
    )
    influence_km = models.DecimalField(
        "Area of input (km2)",
        max_digits=12,
        decimal_places=4,
        null=True,
        blank=True,
        help_text="Area of influence in km2.",
        validators=[MinValueValidator(0)],
    )
    station_file = models.ImageField(
        "Photography",
        upload_to=STATION_IMAGE_PATH,
        null=True,
        blank=True,
        help_text="Photography of the station.",
    )
    station_external = models.BooleanField(
        "External", default=False, help_text="Is the station external?"
    )
    variables = models.CharField(
        "Stored variables",
        max_length=100,
        null=False,
        blank=False,
        default="",
        editable=False,
        help_text="Comma-separated list of variables measured by the station.",
    )

    @property
    def variables_list(self) -> list[str]:
        """Return the list of variables measured by the station.

        Only variables with data in the database are returned.

        Returns:
            list[str]: List of variables measured by the station.
        """
        return self.variables.split(",") if self.variables else []

    def __str__(self) -> str:
        """Return the station code."""
        return str(self.station_code)

    def get_absolute_url(self) -> str:
        """Return the absolute url of the station."""
        return reverse("station:station_detail", kwargs={"pk": self.pk})

    def set_object_permissions(self) -> None:
        """Set object-level permissions.

        This method is called by the save method of the model to set the object-level
        permissions based on the visibility level of the object. In addition to the
        standard permissions for the station, the view_measurements permission is set
        which controls who can view the measurements associated to the station.
        """
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
