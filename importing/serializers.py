from rest_framework import serializers

from .models import DataImport


class DataImportUploadRequestSerializer(serializers.ModelSerializer):
    """Serializer for data import upload request."""

    class Meta:
        model = DataImport
        fields = [
            "station",
            "format",
            "visibility",
            "reprocess",
            "observations",
            "rawfile",
        ]


class DataImportUploadResponseSerializer(serializers.ModelSerializer):
    """Serializer for data import upload response."""

    station = serializers.SlugRelatedField(
        slug_field="station_code",
        read_only=True,
    )

    class Meta:
        model = DataImport
        fields = [
            "data_import_id",  # Primary key field
            "station",
            "format",
            "rawfile",
            "date",  # Auto-generated submission date
            "start_date",  # Auto-filled during processing
            "end_date",  # Auto-filled during processing
            "records",  # Auto-filled during processing
            "observations",
            "status",  # Import status
            "reprocess",
        ]
        read_only_fields = [
            "data_import_id",
            "date",
            "start_date",
            "end_date",
            "records",
            "status",
        ]
