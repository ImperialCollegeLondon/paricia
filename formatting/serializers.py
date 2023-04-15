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
        exclude = []


class DelimiterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Delimiter
        exclude = []


class DateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Date
        exclude = []


class TimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Time
        exclude = []


class FormatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Format
        exclude = []


class ClassificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classification
        exclude = []


class AssociationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Association
        exclude = []
