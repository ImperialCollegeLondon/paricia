from rest_framework import serializers

from .models import DataImportFull, DataImportTemp


class DataImportTempSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
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
            "owner",
        ]


class DataImportFullSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")
    filepath = serializers.ReadOnlyField()

    class Meta:
        model = DataImportFull
        fields = [
            "filepath",
            "import_temp",
            "user",
            "date",
        ]
