from django.contrib import admin

from management.admin import PermissionsBaseAdmin

from .models import DataImport, ImportOrigin, ThingsboardImportMap


@admin.register(DataImport)
class DataImportAdmin(PermissionsBaseAdmin):
    """Admin class for the DataImport model."""

    list_display = [
        "data_import_id",
        "station",
        "format",
        "status",
        "date",
        "start_date",
        "end_date",
        "records",
    ]
    readonly_fields = ["date", "start_date", "end_date", "records", "status", "log"]
    foreign_key_fields = ["station", "format"]
    search_fields = ["station__name", "format__name"]


@admin.register(ThingsboardImportMap)
class ThingsboardImportMapAdmin(admin.ModelAdmin):
    """Admin class for the ThingsboardImportMap model."""

    list_display = ["tb_variable", "variable", "device_id", "station"]
    search_fields = ["tb_variable", "variable__name", "device_id", "station__name"]


@admin.register(ImportOrigin)
class ImportOriginAdmin(admin.ModelAdmin):
    """Admin class for the ImportOrigin model."""
