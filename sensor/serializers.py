from rest_framework import serializers

from .models import Sensor, SensorBrand, SensorType


class SensorTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorType
        exclude = []


class SensorBrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorBrand
        exclude = []


class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        exclude = []
