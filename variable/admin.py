from django.contrib import admin

from management.admin import PermissionsBaseAdmin

from .models import SensorInstallation, Unit, Variable

admin.site.site_header = "Paricia Administration - Variables"


@admin.register(Unit)
class SensorTypeAdmin(PermissionsBaseAdmin):
    """Admin class for the Unit model."""

    list_display = ["unit_id", "name", "owner", "permissions_level"]


@admin.register(Variable)
class VariableAdmin(PermissionsBaseAdmin):
    """Admin class for the Variable model."""

    list_display = [
        "variable_id",
        "variable_code",
        "name",
        "unit",
        "maximum",
        "minimum",
        "diff_warning",
        "diff_error",
        "outlier_limit",
        "is_active",
        "automatic_report",
        "null_limit",
        "nature",
        "owner",
        "permissions_level",
    ]


@admin.register(SensorInstallation)
class SensorInstallationAdmin(PermissionsBaseAdmin):
    """Admin class for the SensorInstallation model."""

    list_display = [
        "sensorinstallation_id",
        "variable",
        "station",
        "sensor",
        "start_date",
        "end_date",
        "state",
        "owner",
        "permissions_level",
    ]
    list_filter = ["variable", "station", "sensor"]
    foreign_key_fields = ["variable", "station", "sensor"]
