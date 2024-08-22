from django.contrib import admin

from management.admin import PermissionsBaseAdmin

from .models import DataImportFull, DataImportTemp

admin.site.site_header = "Paricia Administration - Importing"


@admin.register(DataImportTemp)
class DataImportTempAdmin(PermissionsBaseAdmin):
    """Admin class for the DataImportTemp model."""

    list_display = [
        "data_import_id",
        "station",
        "format",
        "date",
        "start_date",
        "end_date",
    ]
    readonly_fields = ["date", "start_date", "end_date"]
    foreign_key_fields = ["station", "format"]


@admin.register(DataImportFull)
class DataImportFullAdmin(PermissionsBaseAdmin):
    """Admin class for the DataImportFull model."""

    list_display = ["date", "import_temp"]
    readonly_fields = ["date"]
    foreign_key_fields = ["import_temp"]
