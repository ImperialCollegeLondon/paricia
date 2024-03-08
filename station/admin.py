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
    model = "stationtype"
    list_display = ["id", "name", "owner", "permissions_level"]


@admin.register(Country)
class CountryAdmin(PermissionsBaseAdmin):
    model = "country"
    list_display = ["id", "name", "owner", "permissions_level"]


@admin.register(Region)
class RegionAdmin(PermissionsBaseAdmin):
    model = "region"
    list_display = ["id", "name", "country", "owner", "permissions_level"]
    list_filter = ["country"]
    foreign_key_fields = ["country"]


@admin.register(Ecosystem)
class EcosystemAdmin(PermissionsBaseAdmin):
    model = "ecosystem"
    list_display = ["id", "name", "owner", "permissions_level"]


@admin.register(Institution)
class InstitutionAdmin(PermissionsBaseAdmin):
    model = "institution"
    list_display = ["id", "name", "owner", "permissions_level"]


@admin.register(PlaceBasin)
class PlaceBasinAdmin(PermissionsBaseAdmin):
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
    model = "place"
    list_display = ["id", "name", "image", "owner", "permissions_level"]


@admin.register(Basin)
class BasinAdmin(PermissionsBaseAdmin):
    model = "basin"
    list_display = ["id", "name", "image", "file", "owner", "permissions_level"]


@admin.register(Station)
class StationAdmin(PermissionsBaseAdmin):
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
    model = "deltat"
    list_display = ["id", "delta_t", "station", "owner", "permissions_level"]
    list_filter = ["station"]
    foreign_key_fields = ["station"]
