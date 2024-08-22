from rest_framework import serializers

from .models import (
    Association,
    Classification,
    Date,
    Delimiter,
    Extension,
    Format,
    Time,
)


class ExtensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Extension
        exclude: list[str] = []


class DelimiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delimiter
        exclude: list[str] = []


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        exclude: list[str] = []


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        exclude: list[str] = []


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        exclude: list[str] = []


class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        exclude: list[str] = []


class AssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        exclude: list[str] = []
