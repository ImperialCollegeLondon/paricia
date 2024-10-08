import django_tables2 as tables

from .models import Sensor, SensorBrand, SensorType


class SensorTable(tables.Table):
    sensor_id = tables.Column(linkify=True)
    sensor_type = tables.Column(linkify=True)
    sensor_brand = tables.Column(linkify=True)

    class Meta:
        model = Sensor
        fields = [
            "sensor_id",
            "visibility",
            "sensor_code",
            "sensor_type",
            "sensor_brand",
            "status",
        ]


class SensorTypeTable(tables.Table):
    type_id = tables.Column(linkify=True)

    class Meta:
        model = SensorType
        fields = ["type_id", "visibility", "name"]


class SensorBrandTable(tables.Table):
    brand_id = tables.Column(linkify=True)

    class Meta:
        model = SensorBrand
        fields = ["brand_id", "visibility", "name"]
