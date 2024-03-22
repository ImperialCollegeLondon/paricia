from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user

from management.admin import _get_queryset
from measurement.models import Measurement, Report

admin.site.site_header = "Paricia Administration - Measurements"


class MeasurementBaseAdmin(GuardedModelAdmin):
    list_display = ["id", "station", "variable", "maximum", "minimum"]
    list_filter = ["station", "variable"]

    def has_add_permission(self, request):
        """Check if the user has the correct permission to add objects."""
        return request.user.has_perm(
            f"{self.opts.app_label}.add_{self.opts.model_name}"
        )

    def has_change_permission(self, request, obj=None):
        """Check if the user has the correct permission to change the object."""
        if obj is not None:
            return request.user.has_perm("change_station", obj.station)
        return True

    def has_delete_permission(self, request, obj=None):
        """Check if the user has the correct permission to delete the object."""
        if obj is not None:
            return request.user.has_perm("delete_station", obj.station)
        return True

    def has_view_permission(self, request, obj=None):
        """Check if the user has the correct permission to view the object."""
        if obj is not None:
            return request.user.has_perm("view_measurements", obj.station)
        return True

    def get_queryset(self, request):
        """Return a queryset of the objects that the user has view permissions for."""
        qs = super().get_queryset(request)
        stations = get_objects_for_user(request.user, "station.view_measurements")
        return qs.filter(station__in=stations)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """Limit the queryset for foreign key fields."""
        if db_field.name == "station":
            kwargs["queryset"] = get_objects_for_user(
                request.user, "station.change_station"
            )
        elif db_field.name == "variable":
            kwargs["queryset"] = _get_queryset(db_field, request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


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
