from django.contrib import admin
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_perms

from .models import Measurement, Report

admin.site.site_header = "Paricia Administration - Measurements"


class MeasurementBaseAdmin(GuardedModelAdmin):
    list_display = ["id", "station", "variable", "maximum", "minimum"]
    list_filter = ["station", "variable"]

    def has_add_permission(self, request):
        return request.user.is_authenticated

    def has_change_permission(self, request, obj=None):
        if obj is not None:
            return "change_measurementbase" in get_perms(request.user, obj)
        return True

    def has_delete_permission(self, request, obj=None):
        if obj is not None:
            return "delete_measurementbase" in get_perms(request.user, obj)
        return True

    def has_view_permission(self, request, obj=None):
        if obj is not None:
            return "view_measurementbase" in get_perms(request.user, obj)
        return True


@admin.register(Report)
class ReportAdmin(MeasurementBaseAdmin):
    list_display = ["id", "report_type"] + MeasurementBaseAdmin.list_display[1:]
    list_filter = ["report_type"] + MeasurementBaseAdmin.list_filter


@admin.register(Measurement)
class MeasurementAdmin(MeasurementBaseAdmin):
    list_display = [
        "id",
        "is_validated",
        "is_active",
        "overwritten",
    ] + MeasurementBaseAdmin.list_display[1:]
    list_filter = ["is_validated", "is_active"] + MeasurementBaseAdmin.list_filter
    readonly_fields = [r for r in dir(Measurement) if r.startswith("raw_")]
