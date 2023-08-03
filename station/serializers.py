from rest_framework import serializers

from .models import (
    Basin,
    Country,
    DeltaT,
    Ecosystem,
    Institution,
    Place,
    PlaceBasin,
    Region,
    Station,
    StationType,
)


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ["id", "name"]


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        exclude = []


class EcosystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ecosystem
        exclude = []


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        exclude = []


class StationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationType
        exclude = []


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        exclude = []


class BasinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basin
        exclude = []


class PlaceBasinSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceBasin
        exclude = []


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        exclude = []


class DeltaTSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeltaT
        exclude = []
