from rest_framework import serializers

from formatting.models import Format
from station.models import Station

from .models import DataImport


class DataImportUploadRequestSerializer(serializers.Serializer):
    """Serializer for data import upload request."""

    station = serializers.SlugRelatedField(
        slug_field="station_code",
        queryset=Station.objects.all(),
        help_text="Station code",
    )
    format = serializers.PrimaryKeyRelatedField(
        queryset=Format.objects.all(),
        help_text="Format ID",
    )
    visibility = serializers.ChoiceField(
        choices=["public", "private"],
        default="private",
        help_text="Visibility level",
    )
    reprocess = serializers.BooleanField(
        default=False,
        help_text="Reprocess data after import",
    )
    observations = serializers.CharField(
        required=False,
        allow_blank=True,
        help_text="Additional observations",
    )
    rawfile = serializers.FileField(
        help_text="Data file to upload",
    )


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
