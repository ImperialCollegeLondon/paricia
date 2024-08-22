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
        exclude: list[str] = []


class EcosystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ecosystem
        exclude: list[str] = []


class InstitutionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Institution
        exclude: list[str] = []


class StationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StationType
        exclude: list[str] = []


class PlaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Place
        exclude: list[str] = []


class BasinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Basin
        exclude: list[str] = []


class PlaceBasinSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlaceBasin
        exclude: list[str] = []


class StationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Station
        exclude: list[str] = []


class DeltaTSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeltaT
        exclude: list[str] = []
