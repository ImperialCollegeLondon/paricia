from django.contrib import admin

from management.admin import PermissionsBaseAdmin

from .models import (
    Basin,
    Country,
    Ecosystem,
    Institution,
    Place,
    PlaceBasin,
    Region,
    Station,
    StationType,
)


@admin.register(StationType)
class StationTypeAdmin(PermissionsBaseAdmin):
    """Admin class for the StationType model."""

    list_display = ["id", "name", "owner", "visibility"]


@admin.register(Country)
class CountryAdmin(PermissionsBaseAdmin):
    """Admin class for the Country model."""

    list_display = ["id", "name", "owner", "visibility"]


@admin.register(Region)
class RegionAdmin(PermissionsBaseAdmin):
    """Admin class for the Region model."""

    list_display = ["id", "name", "country", "owner", "visibility"]
    list_filter = ["country"]
    foreign_key_fields = ["country"]


@admin.register(Ecosystem)
class EcosystemAdmin(PermissionsBaseAdmin):
    """Admin class for the Ecosystem model."""

    list_display = ["id", "name", "owner", "visibility"]


@admin.register(Institution)
class InstitutionAdmin(PermissionsBaseAdmin):
    """Admin class for the Institution model."""

    list_display = ["id", "name", "owner", "visibility"]


@admin.register(PlaceBasin)
class PlaceBasinAdmin(PermissionsBaseAdmin):
    """Admin class for the PlaceBasin model."""

    list_display = [
        "id",
        "place",
        "basin",
        "image",
        "owner",
        "visibility",
    ]
    list_filter = ["place", "basin"]
    foreign_key_fields = ["place", "basin"]


@admin.register(Place)
class PlaceAdmin(PermissionsBaseAdmin):
    """Admin class for the Place model."""

    list_display = ["id", "name", "image", "owner", "visibility"]


@admin.register(Basin)
class BasinAdmin(PermissionsBaseAdmin):
    """Admin class for the Basin model."""

    list_display = ["id", "name", "image", "file", "owner", "visibility"]


@admin.register(Station)
class StationAdmin(PermissionsBaseAdmin):
    """Admin class for the Station model."""

    limit_visibility_level = False
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
        "visibility",
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
