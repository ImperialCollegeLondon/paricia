from rest_framework import serializers

from .models import DataImportFull, DataImportTemp


class DataImportFullSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    start_date = serializers.ReadOnlyField()
    end_date = serializers.ReadOnlyField()
    station = serializers.ReadOnlyField()
    format = serializers.ReadOnlyField()
    observations = serializers.ReadOnlyField()

    class Meta:
        model = DataImportFull
        fields = [
            "data_import_id",
            "station",
            "format",
            "start_date",
            "end_date",
            "date",
            "observations",
            "file",
            "user",
            "import_temp",
        ]


class DataImportTempSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    start_date = serializers.ReadOnlyField()
    end_date = serializers.ReadOnlyField()

    class Meta:
        model = DataImportTemp
        fields = [
            "data_import_id",
            "station",
            "format",
            "start_date",
            "end_date",
            "date",
            "observations",
            "file",
            "user",
        ]
