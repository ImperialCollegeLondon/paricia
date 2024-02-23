from django.contrib import admin
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
