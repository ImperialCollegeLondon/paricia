from rest_framework import serializers

from .models import SensorInstallation, Unit, Variable


class UnitSerializer(serializers.ModelSerializer):
    """Serializer for the Unit model."""

    class Meta:
        model = Unit
        exclude: list[str] = []


class VariableSerializer(serializers.ModelSerializer):
    """Serializer for the Variable model."""

    class Meta:
        model = Variable
        exclude: list[str] = []


class SensorInstallationSerializer(serializers.ModelSerializer):
    """Serializer for the SensorInstallation model."""

    class Meta:
        model = SensorInstallation
        exclude: list[str] = []
