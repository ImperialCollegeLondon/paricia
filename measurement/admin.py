from django.contrib import admin

from .models import Measurement, Report

admin.site.site_header = "Paricia Administration - Measurements"


class MeasurementBaseAdmin(admin.ModelAdmin):
    list_display = ["id", "station", "variable", "maximum", "minimum"]
    list_filter = ["station", "variable"]


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
