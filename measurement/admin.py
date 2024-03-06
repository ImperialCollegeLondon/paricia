from django.contrib import admin
from django.core.exceptions import PermissionDenied
from guardian.shortcuts import get_perms

from management.admin import PermissionsBaseAdmin
from measurement.models import Measurement, Report
from station.models import Station

admin.site.site_header = "Paricia Administration - Measurements"


class MeasurementBaseAdmin(PermissionsBaseAdmin):
    list_display = ["id", "station", "variable", "maximum", "minimum"]
    list_filter = ["station", "variable"]

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "station":
            kwargs["queryset"] = Station.objects.filter(owner=request.user)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_view_permission(self, request, obj=None):
        if obj is not None:
            return f"view_{self.model}" in get_perms(request.user, obj)
        return True

    def save_model(self, request, obj, form, change):
        if obj.station.owner != request.user:
            raise PermissionDenied("You are not the owner of this station.")
        super().save_model(request, obj, form, change)


@admin.register(Report)
class ReportAdmin(MeasurementBaseAdmin):
    model = "report"
    list_display = ["id", "report_type"] + MeasurementBaseAdmin.list_display[1:]
    list_filter = ["report_type"] + MeasurementBaseAdmin.list_filter


@admin.register(Measurement)
class MeasurementAdmin(MeasurementBaseAdmin):
    model = "measurement"
    list_display = [
        "id",
        "is_validated",
        "is_active",
        "overwritten",
    ] + MeasurementBaseAdmin.list_display[1:]
    list_filter = ["is_validated", "is_active"] + MeasurementBaseAdmin.list_filter
    readonly_fields = [r for r in dir(Measurement) if r.startswith("raw_")]
