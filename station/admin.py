from django.contrib import admin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_perms

from .models import Station

admin.site.site_header = "Paricia Administration - Stations"


@admin.register(Station)
class StationAdmin(GuardedModelAdmin):
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
        "station_state",
        "station_latitude",
        "station_longitude",
        "station_altitude",
        "station_external",
        "influence_km",
        "timezone",
    ]
    list_filter = ["station_type", "country", "region", "ecosystem", "institution"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name in [
            "station_type",
            "country",
            "region",
            "ecosystem",
            "institution",
        ]:
            kwargs["queryset"] = get_queryset(db_field.related_model, request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        return request.user.is_authenticated

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return "change_station" in get_perms(request.user, obj)
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return "delete_station" in get_perms(request.user, obj)
        return True

    def has_view_permission(self, request, obj=None):
        if obj is not None:
            return "view_station" in get_perms(request.user, obj)
        return True

    def save_model(self, request, obj, form, change):
        fields = ["station_type", "country", "region", "ecosystem", "institution"]
        for field in fields:
            owner = getattr(obj, field).owner
            perm_level = getattr(obj, field).permissions_level
            if owner != request.user and perm_level == "Private":
                raise PermissionDenied(f"Private {field}: Only owner can use.")

        super().save_model(request, obj, form, change)


def get_queryset(model, user):
    return model.objects.filter(Q(owner=user) | Q(permissions_level="Public"))
