from rest_framework import serializers

from .models import Sensor, SensorBrand, SensorType


class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        exclude: list[str] = []


class SensorBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorBrand
        exclude: list[str] = []


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        exclude: list[str] = []
