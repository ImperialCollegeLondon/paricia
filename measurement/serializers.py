from rest_framework import serializers

from station.models import Station
from variable.models import Variable


class MeasurementDataDownloadRequestSerializer(serializers.Serializer):
    """Serializer for validating measurement data download requests."""

    REPORT_TYPE_CHOICES = [
        ("measurement", "Raw measurement"),
        ("validated", "Validated measurement"),
        ("hourly", "Hourly report"),
        ("daily", "Daily report"),
        ("monthly", "Monthly report"),
    ]

    TRACE_CHOICES = [
        ("value", "Value"),
        ("maximum", "Maximum"),
        ("minimum", "Minimum"),
        ("depth", "Depth"),
        ("direction", "Direction"),
    ]

    station = serializers.SlugRelatedField(
        slug_field="station_code",
        queryset=Station.objects.all(),
        help_text="Station code for the data to download.",
    )
    variable = serializers.SlugRelatedField(
        slug_field="variable_code",
        queryset=Variable.objects.all(),
        help_text="Variable code for the data to download.",
    )
    start_date = serializers.DateField(
        help_text="Start date for the data range (YYYY-MM-DD)."
    )
    end_date = serializers.DateField(
        help_text="End date for the data range (YYYY-MM-DD)."
    )
    report_type = serializers.ChoiceField(
        choices=REPORT_TYPE_CHOICES,
        help_text="Type of data to retrieve.",
    )
    traces = serializers.MultipleChoiceField(
        choices=TRACE_CHOICES,
        default=[
            "value",
            "maximum",
            "minimum",
            "depth",
            "direction",
        ],
        help_text="Data traces to include in the response.",
    )

    def validate(self, attrs):
        """Validate the request data."""
        if attrs["start_date"] > attrs["end_date"]:
            raise serializers.ValidationError(
                {"end_date": "End date must be after start date."}
            )

        # Validate that the variable is available for the station
        station = attrs["station"]
        variable = attrs["variable"]
        if variable.variable_code not in station.variables_list:
            raise serializers.ValidationError(
                {
                    "variable": f"Variable '{variable.variable_code}' is not available "
                    f"for station '{station.station_code}'."
                }
            )

        return attrs


class MeasurementDataDownloadResponseSerializer(serializers.Serializer):
    """Serializer for measurement data response."""

    id = serializers.IntegerField(read_only=True)
    time = serializers.DateTimeField(read_only=True)
    value = serializers.DecimalField(
        max_digits=14, decimal_places=4, read_only=True, required=False
    )
    maximum = serializers.DecimalField(
        max_digits=14, decimal_places=4, read_only=True, required=False
    )
    minimum = serializers.DecimalField(
        max_digits=14, decimal_places=4, read_only=True, required=False
    )
    depth = serializers.DecimalField(
        max_digits=14, decimal_places=4, read_only=True, required=False
    )
    direction = serializers.DecimalField(
        max_digits=14, decimal_places=4, read_only=True, required=False
    )
    completeness = serializers.DecimalField(
        max_digits=4, decimal_places=1, read_only=True, required=False
    )
    report_type = serializers.CharField(read_only=True, required=False)
