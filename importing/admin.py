from django.contrib import admin

from management.admin import PermissionsBaseAdmin

from .models import DataImport


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
