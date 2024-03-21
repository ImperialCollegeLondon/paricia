from django.contrib import admin
from django.core.exceptions import PermissionDenied
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user, get_perms

from measurement.models import Measurement, Report
from station.models import Station

admin.site.site_header = "Paricia Administration - Measurements"


class MeasurementBaseAdmin(GuardedModelAdmin):
    list_display = ["id", "station", "variable", "maximum", "minimum"]
    list_filter = ["station", "variable"]

    def has_add_permission(self, request):
        """Allow all authenticated users to add objects."""
        return request.user.is_authenticated

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

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit the list of stations available based on permssions."""
        if db_field.name == "station":
            kwargs["queryset"] = get_objects_for_user(
                request.user, "station.change_station"
            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def save_model(self, request, obj, form, change):
        """Check if the user has the correct permissions to save the object."""
        if "change_station" not in get_perms(request.user, obj.station):
            raise PermissionDenied("You are not the owner of this station.")
        super().save_model(request, obj, form, change)


@admin.register(Report)
class ReportAdmin(MeasurementBaseAdmin):
    """Admin class for the Report model."""

    model = "report"
    list_display = ["id", "report_type"] + MeasurementBaseAdmin.list_display[1:]
    list_filter = ["report_type"] + MeasurementBaseAdmin.list_filter


@admin.register(Measurement)
class MeasurementAdmin(MeasurementBaseAdmin):
    """Admin class for the Measurement model."""

    model = "measurement"
    list_display = [
        "id",
        "is_validated",
        "is_active",
        "overwritten",
    ] + MeasurementBaseAdmin.list_display[1:]
    list_filter = ["is_validated", "is_active"] + MeasurementBaseAdmin.list_filter
    readonly_fields = [r for r in dir(Measurement) if r.startswith("raw_")]
