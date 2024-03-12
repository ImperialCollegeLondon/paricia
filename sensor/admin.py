from django.contrib import admin

from management.admin import PermissionsBaseAdmin

from .models import Sensor, SensorBrand, SensorType

admin.site.site_header = "Paricia Administration - Sensors"


@admin.register(SensorType)
class SensorTypeAdmin(PermissionsBaseAdmin):
    """Admin class for the SensorType model."""

    model = "sensortype"
    list_display = ["type_id", "name", "owner", "permissions_level"]


@admin.register(SensorBrand)
class SensorBrandAdmin(PermissionsBaseAdmin):
    """Admin class for the SensorBrand model."""

    model = "sensorbrand"
    list_display = ["brand_id", "name", "owner", "permissions_level"]


@admin.register(Sensor)
class SensorAdmin(PermissionsBaseAdmin):
    """Admin class for the Sensor model."""

    model = "sensor"
    list_display = [
        "sensor_id",
        "code",
        "model",
        "serial",
        "status",
        "owner",
        "permissions_level",
    ]
    list_filter = ["sensor_brand", "sensor_type"]
    foreign_key_fields = ["sensor_brand", "sensor_type"]
