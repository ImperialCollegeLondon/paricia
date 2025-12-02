########################################################################################
# Plataforma para la Iniciativa Regional de Monitoreo Hidrológico de Ecosistemas Andinos
# (iMHEA)basada en los desarrollos realizados por:
#     1) FONDO PARA LA PROTECCIÓN DEL AGUA (FONAG), Ecuador.
#           Contacto: info@fonag.org.ec
#     2) EMPRESA PÚBLICA METROPOLITANA DE AGUA POTABLE Y SANEAMIENTO DE QUITO (EPMAPS),
#           Ecuador.
#           Contacto: paramh2o@aguaquito.gob.ec
#
#  IMPORTANTE: Mantener o incluir esta cabecera con la mención de las instituciones
#  creadoras, ya sea en uso total o parcial del código.
########################################################################################

from django.shortcuts import render
from django.views import View
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from guardian.mixins import LoginRequiredMixin
from guardian.shortcuts import get_objects_for_user
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from station.models import Station

from .reporting import get_report_data_from_db
from .serializers import (
    MeasurementDataRequestSerializer,
    MeasurementDataResponseSerializer,
)


class DailyValidation(LoginRequiredMixin, View):
    """View for displaying the Daily Validation dash app."""

    def get(self, request, *args, **kwargs):
        from .dash_apps import daily_validation  # noqa

        stations = get_objects_for_user(request.user, "change_station", klass=Station)
        station_codes = list(stations.values_list("station_code", flat=True))
        context = {"django_context": {"stations_list": {"children": station_codes}}}
        return render(request, "daily_validation.html", context)


class DataReport(View):
    """View for displaying the Data Report dash app."""

    def get(self, request, *args, **kwargs):
        from .dash_apps import data_report  # noqa

        stations = get_objects_for_user(
            request.user, "view_measurements", klass=Station
        )
        station_codes = list(stations.values_list("station_code", flat=True))
        context = {"django_context": {"stations_list": {"children": station_codes}}}
        return render(request, "data_report.html", context)


class MeasurementDataAPIView(APIView):
    """API endpoint for downloading measurement data.

    Users can only access data from stations they have view_measurements permission for.
    """

    permission_classes = [IsAuthenticated]

    def get_permitted_stations(self, user):
        """Get stations the user has permission to view measurements for."""
        return get_objects_for_user(user, "view_measurements", klass=Station)

    @extend_schema(
        summary="Download measurement data",
        description="""
        Download measurement data within a date range.

        **Permissions**: Users can only access data from stations they have
        `view_measurements` permission for.

        **Report Types**:
        - `measurement`: Raw measurement data
        - `validated`: Validated measurement data only
        - `hourly`: Hourly aggregated report
        - `daily`: Daily aggregated report
        - `monthly`: Monthly aggregated report

        **Traces**: Select which data columns to include in the response.
        Common traces include `value`, `maximum`, `minimum`, `depth`, and `direction`.
        """,
        parameters=[
            OpenApiParameter(
                name="station",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Station code",
                required=True,
            ),
            OpenApiParameter(
                name="variable",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Variable code",
                required=True,
            ),
            OpenApiParameter(
                name="start_date",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Start date (YYYY-MM-DD)",
                required=True,
            ),
            OpenApiParameter(
                name="end_date",
                type=str,
                location=OpenApiParameter.QUERY,
                description="End date (YYYY-MM-DD)",
                required=True,
            ),
            OpenApiParameter(
                name="report_type",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Type of report",
                required=True,
                enum=["measurement", "validated", "hourly", "daily", "monthly"],
            ),
            OpenApiParameter(
                name="traces",
                type={"type": "array", "items": {"type": "string"}},
                location=OpenApiParameter.QUERY,
                description="Data traces to include",
                required=False,
                enum=["value", "maximum", "minimum", "depth", "direction"],
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=MeasurementDataResponseSerializer(many=True),
                description="Measurement data retrieved successfully",
                examples=[
                    OpenApiExample(
                        "Successful response",
                        value=[
                            {
                                "id": 1,
                                "time": "2024-01-01T00:00:00Z",
                                "value": "12.5000",
                                "maximum": "15.0000",
                                "minimum": "10.0000",
                            },
                            {
                                "id": 2,
                                "time": "2024-01-01T01:00:00Z",
                                "value": "13.2000",
                                "maximum": "16.0000",
                                "minimum": "11.0000",
                            },
                        ],
                    )
                ],
            ),
            400: OpenApiResponse(description="Invalid request parameters"),
            403: OpenApiResponse(
                description="User does not have permission to access the station's data"
            ),
            404: OpenApiResponse(description="Station or variable not found"),
        },
        tags=["measurements"],
    )
    def get(self, request):
        """Retrieve measurement data based on query parameters."""
        # Handle traces as a list from query params
        traces = request.query_params.getlist("traces", ["value"])

        # Build data dict for serializer
        data = {
            "station": request.query_params.get("station"),
            "variable": request.query_params.get("variable"),
            "start_date": request.query_params.get("start_date"),
            "end_date": request.query_params.get("end_date"),
            "report_type": request.query_params.get("report_type"),
            "traces": traces,
        }

        # Validate request parameters
        serializer = MeasurementDataRequestSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        station = validated_data["station"]

        # Check user permissions for this station
        permitted_stations = self.get_permitted_stations(request.user)
        if station not in permitted_stations:
            return Response(
                {
                    "detail": "You do not have permission to access data "
                    f"for station '{station.station_code}'."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get the data using existing function
        try:
            df = get_report_data_from_db(
                station=station.station_code,
                variable=validated_data["variable"].variable_code,
                start_time=validated_data["start_date"].strftime("%Y-%m-%d"),
                end_time=validated_data["end_date"].strftime("%Y-%m-%d"),
                report_type=validated_data["report_type"],
                whole_months=False,
            )
        except Exception as e:
            return Response(
                {"detail": f"Error retrieving data: {e!s}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        if df.empty:
            return Response([])

        # Filter to requested traces plus required columns
        available_traces = [t for t in validated_data["traces"] if t in df.columns]
        columns_to_include = ["id", "time", *available_traces]

        # Add completeness and report_type if available (for report data)
        if "completeness" in df.columns:
            columns_to_include.append("completeness")
        if "report_type" in df.columns:
            columns_to_include.append("report_type")

        # Filter columns that exist in the dataframe
        columns_to_include = [c for c in columns_to_include if c in df.columns]
        result_df = df[columns_to_include]

        # Convert to list of dicts for response
        result = result_df.to_dict(orient="records")

        return Response(result)
