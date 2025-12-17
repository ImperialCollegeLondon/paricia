from rest_framework import serializers

from station.models import Station

from .models import DataImport


class DataImportUploadRequestSerializer(serializers.ModelSerializer):
    """Serializer for data import upload request."""

    station = serializers.SlugRelatedField(
        slug_field="station_code",
        queryset=Station.objects.all(),
    )

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
    status_display = serializers.SerializerMethodField(read_only=True)

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
            "status_display",  # Import status
            "reprocess",
        ]
        read_only_fields = [
            "data_import_id",
            "date",
            "start_date",
            "end_date",
            "records",
            "status_display",
        ]

    def get_status_display(self, obj):
        return (
            obj.get_status_display()
            if hasattr(obj, "get_status_display")
            else obj.status
        )


class DataImportDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer used when the requesting user is the owner.

    Includes the ingestion `log` so clients can debug failures.
    """

    station = serializers.SlugRelatedField(
        slug_field="station_code",
        read_only=True,
    )
    status_display = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = DataImport
        fields = [
            "data_import_id",
            "station",
            "format",
            "rawfile",
            "date",
            "start_date",
            "end_date",
            "records",
            "observations",
            "status",
            "status_display",
            "reprocess",
        ]
        read_only_fields = [
            "data_import_id",
            "date",
            "start_date",
            "end_date",
            "records",
            "status",
            "status_display",
        ]

    def get_status_display(self, obj):
        return (
            obj.get_status_display()
            if hasattr(obj, "get_status_display")
            else obj.status
        )
