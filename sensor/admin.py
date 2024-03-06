from django.contrib import admin

from management.admin import PermissionsBaseAdmin

from .models import Sensor, SensorBrand, SensorType

admin.site.site_header = "Paricia Administration - Sensors"


@admin.register(SensorType)
class SensorTypeAdmin(PermissionsBaseAdmin):
    model = "sensortype"
    list_display = ["name", "type_id", "owner", "permissions_level"]


@admin.register(SensorBrand)
class SensorBrandAdmin(PermissionsBaseAdmin):
    model = "sensorbrand"
    list_display = ["name", "brand_id", "owner", "permissions_level"]


@admin.register(Sensor)
class SensorAdmin(PermissionsBaseAdmin):
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
