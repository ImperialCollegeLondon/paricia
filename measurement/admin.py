from django.contrib import admin

from .models import Report

admin.site.site_header = "Paricia Administration - Measurements"


class MeasurementBaseAdmin(admin.ModelAdmin):
    list_display = ["id", "station", "variable", "maximum", "minimum"]
    list_filter = ["station", "variable"]


@admin.register(Report)
class ReportAdmin(MeasurementBaseAdmin):
    list_display = ["report_type"] + MeasurementBaseAdmin.list_display
    list_filter = ["report_type"] + MeasurementBaseAdmin.list_filter
