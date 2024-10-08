from django.contrib import admin

from management.admin import PermissionsBaseAdmin

from .models import SensorInstallation, Unit, Variable


@admin.register(Unit)
class SensorTypeAdmin(PermissionsBaseAdmin):
    """Admin class for the Unit model."""

    list_display = ["unit_id", "name", "owner", "visibility"]


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
        "diff_error",
        "outlier_limit",
        "null_limit",
        "nature",
        "owner",
        "visibility",
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
        "visibility",
    ]
    list_filter = ["variable", "station", "sensor"]
    foreign_key_fields = ["variable", "station", "sensor"]
