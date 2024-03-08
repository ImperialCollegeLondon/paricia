from django.contrib import admin

from management.admin import PermissionsBaseAdmin

from .models import SensorInstallation, Unit, Variable

admin.site.site_header = "Paricia Administration - Variables"


@admin.register(Unit)
class SensorTypeAdmin(PermissionsBaseAdmin):
    model = "unit"
    list_display = ["name", "unit_id", "owner", "permissions_level"]


@admin.register(Variable)
class SensorBrandAdmin(PermissionsBaseAdmin):
    model = "variable"
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
    ]


@admin.register(SensorInstallation)
class SensorAdmin(PermissionsBaseAdmin):
    model = "sensor_installation"
    list_display = [
        "sensorinstallation_id",
        "variable",
        "station",
        "sensor",
        "start_date",
        "end_date",
        "state",
    ]
    list_filter = ["variable", "station", "sensor"]
    foreign_key_fields = ["variable", "station", "sensor"]
