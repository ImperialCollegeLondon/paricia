from rest_framework import serializers

from .models import DataImportFull, DataImportTemp


class DataImportFullSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataImportFull
        fields = [
            "data_import_id",
            "station",
            "format",
            "date",
            "observations",
            "file",
        ]


class DataImportTempSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataImportTemp
        fields = [
            "data_import_id",
            "station",
            "format",
            "date",
            "observations",
            "file",
        ]
