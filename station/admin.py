from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_perms

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

admin.site.site_header = "Paricia Administration - Stations"


class BaseAdmin(GuardedModelAdmin):
    foreign_key_fields: list[str] = []

    def has_add_permission(self, request):
        return request.user.is_authenticated

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return f"change_{self.model}" in get_perms(request.user, obj)
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return f"delete_{self.model}" in get_perms(request.user, obj)
        return True

    def has_view_permission(self, request, obj=None):
        return True

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in self.foreign_key_fields:
            kwargs["queryset"] = _get_queryset(db_field.related_model, request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        for field in self.foreign_key_fields:
            owner = getattr(obj, field).owner
            perm_level = getattr(obj, field).permissions_level
            if owner != request.user and perm_level == "Private":
                raise PermissionDenied(f"Private {field}: Only owner can use.")
        super().save_model(request, obj, form, change)


@admin.register(StationType)
class StationTypeAdmin(BaseAdmin):
    model = "stationtype"
    list_display = ["name", "id", "owner", "permissions_level"]


@admin.register(Country)
class CountryAdmin(BaseAdmin):
    model = "country"
    list_display = ["name", "id", "owner", "permissions_level"]


@admin.register(Region)
class RegionAdmin(BaseAdmin):
    model = "region"
    list_display = ["name", "id", "owner", "permissions_level", "country"]
    list_filter = ["country"]
    foreign_key_fields = ["country"]


@admin.register(Ecosystem)
class EcosystemAdmin(BaseAdmin):
    model = "ecosystem"
    list_display = ["name", "id", "owner", "permissions_level"]


@admin.register(Institution)
class InstitutionAdmin(BaseAdmin):
    model = "institution"
    list_display = ["name", "id", "owner", "permissions_level"]


@admin.register(PlaceBasin)
class PlaceBasinAdmin(BaseAdmin):
    model = "placebasin"
    list_display = [
        "name",
        "id",
        "owner",
        "permissions_level",
        "place",
        "basin",
        "image",
    ]
    list_filter = ["place", "basin"]
    foreign_key_fields = ["place", "basin"]


@admin.register(Place)
class PlaceAdmin(BaseAdmin):
    model = "place"
    list_display = ["name", "id", "owner", "permissions_level", "image"]


@admin.register(Basin)
class BasinAdmin(BaseAdmin):
    model = "basin"
    list_display = ["name", "id", "owner", "permissions_level", "image", "file"]


@admin.register(Station)
class StationAdmin(BaseAdmin):
    model = "station"
    list_display = [
        "station_id",
        "station_code",
        "owner",
        "permissions_level",
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


def _get_queryset(model, user):
    return model.objects.filter(Q(owner=user) | Q(permissions_level="Public"))
