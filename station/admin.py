from django.contrib import admin

from management.admin import PermissionsBaseAdmin

from .models import (
    Basin,
    Country,
    DeltaT,
    Ecosystem,
    Institution,
    Place,
    PlaceBasin,
    Region,
    Station,
    StationType,
)

admin.site.site_header = "Paricia Administration - Stations"


@admin.register(StationType)
class StationTypeAdmin(PermissionsBaseAdmin):
    """Admin class for the StationType model."""

    model = "stationtype"
    list_display = ["id", "name", "owner", "permissions_level"]


@admin.register(Country)
class CountryAdmin(PermissionsBaseAdmin):
    """Admin class for the Country model."""

    model = "country"
    list_display = ["id", "name", "owner", "permissions_level"]


@admin.register(Region)
class RegionAdmin(PermissionsBaseAdmin):
    """Admin class for the Region model."""

    model = "region"
    list_display = ["id", "name", "country", "owner", "permissions_level"]
    list_filter = ["country"]
    foreign_key_fields = ["country"]


@admin.register(Ecosystem)
class EcosystemAdmin(PermissionsBaseAdmin):
    """Admin class for the Ecosystem model."""

    model = "ecosystem"
    list_display = ["id", "name", "owner", "permissions_level"]


@admin.register(Institution)
class InstitutionAdmin(PermissionsBaseAdmin):
    """Admin class for the Institution model."""

    model = "institution"
    list_display = ["id", "name", "owner", "permissions_level"]


@admin.register(PlaceBasin)
class PlaceBasinAdmin(PermissionsBaseAdmin):
    """Admin class for the PlaceBasin model."""

    model = "placebasin"
    list_display = [
        "id",
        "place",
        "basin",
        "image",
        "owner",
        "permissions_level",
    ]
    list_filter = ["place", "basin"]
    foreign_key_fields = ["place", "basin"]


@admin.register(Place)
class PlaceAdmin(PermissionsBaseAdmin):
    """Admin class for the Place model."""

    model = "place"
    list_display = ["id", "name", "image", "owner", "permissions_level"]


@admin.register(Basin)
class BasinAdmin(PermissionsBaseAdmin):
    """Admin class for the Basin model."""

    model = "basin"
    list_display = ["id", "name", "image", "file", "owner", "permissions_level"]


@admin.register(Station)
class StationAdmin(PermissionsBaseAdmin):
    """Admin class for the Station model."""

    model = "station"
    list_display = [
        "station_id",
        "station_code",
        "station_name",
        "station_type",
        "country",
        "region",
        "ecosystem",
        "institution",
        "place_basin",
        "station_state",
        "station_latitude",
        "station_longitude",
        "station_altitude",
        "station_external",
        "influence_km",
        "timezone",
        "owner",
        "permissions_level",
    ]
    list_filter = [
        "station_type",
        "country",
        "region",
        "ecosystem",
        "institution",
    ]
    foreign_key_fields = [
        "station_type",
        "country",
        "region",
        "ecosystem",
        "institution",
        "place_basin",
    ]


@admin.register(DeltaT)
class DeltaTAdmin(PermissionsBaseAdmin):
    """Admin class for the DeltaT model."""

    model = "deltat"
    list_display = ["id", "delta_t", "station", "owner", "permissions_level"]
    list_filter = ["station"]
    foreign_key_fields = ["station"]
