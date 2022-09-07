from rest_framework import serializers

from .models import SensorInstallation, Unit, Variable


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        exclude = []


class VariableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variable
        exclude = []


class SensorInstallationSerializer(serializers.ModelSerializer):
    class Meta:
        depth = 2
        model = SensorInstallation
        exclude = []

class SensorInstallationSerializerUpdate(serializers.ModelSerializer):
    class Meta:
        model = SensorInstallation
        exclude = []

class SensorInstallationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SensorInstallation
        exclude = []
