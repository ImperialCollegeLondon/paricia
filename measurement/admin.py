from django.contrib import admin
from guardian.shortcuts import get_objects_for_user, get_perms

from management.admin import PermissionsBaseAdmin
from measurement.models import Measurement, Report

admin.site.site_header = "Paricia Administration - Measurements"


class MeasurementBaseAdmin(PermissionsBaseAdmin):
    list_display = ["id", "station", "variable", "maximum", "minimum"]
    list_filter = ["station", "variable"]
    foreign_key_fields = ["station", "variable"]

    def has_change_permission(self, request, obj=None):
        """Check if the user has the correct permission to change the object."""
        if obj is not None:
            return "change_station" in get_perms(request.user, obj.station)
        return True

    def has_delete_permission(self, request, obj=None):
        """Check if the user has the correct permission to delete the object."""
        if obj is not None:
            return "delete_station" in get_perms(request.user, obj.station)
        return True

    def has_view_permission(self, request, obj=None):
        """Check if the user has the correct permission to view the object."""
        if obj is not None:
            return "view_measurements" in get_perms(request.user, obj.station)
        return True

    def get_queryset(self, request):
        """Return a queryset of the objects that the user has view permissions for."""
        qs = super().get_queryset(request)
        stations = get_objects_for_user(request.user, "station.view_measurements")
        return qs.filter(station__in=stations)


@admin.register(Report)
class ReportAdmin(MeasurementBaseAdmin):
    """Admin class for the Report model."""

    list_display = ["id", "report_type"] + MeasurementBaseAdmin.list_display[1:]
    list_filter = ["report_type"] + MeasurementBaseAdmin.list_filter


@admin.register(Measurement)
class MeasurementAdmin(MeasurementBaseAdmin):
    """Admin class for the Measurement model."""

    list_display = [
        "id",
        "is_validated",
        "is_active",
        "overwritten",
    ] + MeasurementBaseAdmin.list_display[1:]
    list_filter = ["is_validated", "is_active"] + MeasurementBaseAdmin.list_filter
    readonly_fields = [r for r in dir(Measurement) if r.startswith("raw_")]
