import logging

from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    OpenApiTypes,
    extend_schema,
)
from guardian.shortcuts import get_objects_for_user
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from management.views import (
    CustomCreateView,
    CustomDeleteView,
    CustomDetailView,
    CustomEditView,
    CustomTableView,
)
from station.models import Station

from .filters import DataImportFilter
from .models import DataImport
from .serializers import (
    DataImportDetailSerializer,
    DataImportUploadRequestSerializer,
    DataImportUploadResponseSerializer,
)
from .tables import DataImportTable


class DataImportDetailView(CustomDetailView):
    """View to view a data import."""

    model = DataImport


class DataImportListView(CustomTableView):
    """View to list all data imports."""

    model = DataImport
    table_class = DataImportTable
    filterset_class = DataImportFilter


class DataImportEditView(CustomEditView):
    """View to edit a data import."""

    model = DataImport
    fields = ["visibility", "station", "format", "rawfile", "reprocess", "observations"]
    foreign_key_fields = ["station", "format"]


class DataImportCreateView(CustomCreateView):
    """View to create a data import."""

    model = DataImport
    fields = ["visibility", "station", "format", "rawfile", "reprocess", "observations"]
    foreign_key_fields = ["station", "format"]


class DataImportDeleteView(CustomDeleteView):
    """View to delete a data import."""

    model = DataImport


class DataImportUploadAPIView(APIView):
    """API endpoint for uploading data files for import.

    Access is controlled via object-level permissions using django-guardian.
    Users can only upload data for Station objects for which they have the
    `change_station` permission assigned.
    """

    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # Add this line

    def get_permitted_stations(self, user):
        """Get stations the user has permission to import data for."""
        return get_objects_for_user(user, "change_station", klass=Station)

    @extend_schema(
        summary="Upload data file for import",
        description="""
        Upload a data file to create a new data import.

        **Permissions**: Users can only upload data for stations they have
        `change_station` permission for.

        **File Upload**: Send as multipart/form-data with all parameters in the body.

        **Reprocess**: Set to `true` to reprocess the data after import.
        """,
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "station": {
                        "type": "string",
                        "description": "Station code",
                    },
                    "format": {
                        "type": "integer",
                        "description": "Format ID",
                    },
                    "rawfile": {
                        "type": "string",
                        "format": "binary",
                        "description": "Data file to upload",
                    },
                    "visibility": {
                        "type": "string",
                        "enum": ["public", "private"],
                        "default": "private",
                        "description": "Visibility level",
                    },
                    "reprocess": {
                        "type": "boolean",
                        "default": False,
                        "description": "Reprocess data after import",
                    },
                    "observations": {
                        "type": "string",
                        "description": "Additional observations",
                    },
                },
                "required": ["station", "format", "rawfile"],
            }
        },
        responses={
            201: OpenApiResponse(
                response=DataImportUploadResponseSerializer,
                description="Data import created successfully",
                examples=[
                    OpenApiExample(
                        "Successful upload",
                        value={
                            "data_import_id": 123,
                            "station": "CAR_02_HC_01",
                            "format": 47,
                            "rawfile": "/media/imports/data_2024.csv",
                            "visibility": "private",
                            "reprocess": True,
                            "date": "2024-12-09T10:30:00Z",
                            "status": "N",
                            "status_display": "Not queued",
                        },
                    )
                ],
            ),
            400: OpenApiResponse(description="Invalid request parameters or file"),
            403: OpenApiResponse(
                description="User does not have permission to upload data."
            ),
            404: OpenApiResponse(description="Station or format not found"),
        },
        tags=["importing"],
    )
    def post(self, request):
        """Upload a data file and create a data import."""
        # Get the uploaded file
        rawfile = request.FILES.get("rawfile")
        if not rawfile:
            return Response(
                {"rawfile": ["No file was submitted."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Build data dict for serializer
        data = {
            "station": request.data.get("station"),
            "format": request.data.get("format"),
            "visibility": request.data.get("visibility", "private"),
            "reprocess": request.data.get("reprocess", False),
            "observations": request.data.get("observations", ""),
            "rawfile": rawfile,
        }

        # Validate request parameters
        serializer = DataImportUploadRequestSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        station = validated_data["station"]

        # Check user permissions for this station
        permitted_stations = self.get_permitted_stations(request.user)
        if station not in permitted_stations:
            return Response(
                {
                    "detail": "You do not have permission to upload data "
                    f"for station '{station.station_code}'."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Create the data import
        try:
            data_import = DataImport.objects.create(
                station=station,
                format=validated_data["format"],
                visibility=validated_data["visibility"],
                reprocess=validated_data["reprocess"],
                observations=validated_data.get("observations", ""),
                rawfile=validated_data["rawfile"],
                owner=request.user,
            )
        except Exception as e:
            logging.exception(f"Error creating data import: {e}")
            return Response(
                {"detail": "An internal error occurred while creating data import."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Return the created import
        response_serializer = DataImportUploadResponseSerializer(
            data_import, context={"request": request}
        )
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


class DataIngestionQueryView(APIView):
    """API endpoint for querying data ingestion status/list.

    - No `data_import_id` query param: return list of imports the user may view.
    - With `data_import_id`: only the owner may request detailed info (including `log`).
      Non-owners receive 403 for direct PK detail requests; they should use the list endpoint.
    """  # noqa: E501

    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Query data ingestion status",
        description="""
        - If `data_import_id` query parameter is provided, the endpoint returns the
          details for that DataImport **only if the requesting user is the owner**.
          Owners receive the full detail including the ingestion `log`.
        - If no `data_import_id` is provided, the endpoint returns a list of
          DataImport objects the user can view, ordered by submission date.
        """,
        parameters=[
            OpenApiParameter(
                name="data_import_id",
                type=OpenApiTypes.INT,
                location=OpenApiParameter.QUERY,
                required=False,
                description="Primary key of a DataImport to return detailed info.",
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Data ingestion status retrieved successfully"
            ),
            400: OpenApiResponse(description="Invalid request parameters"),
            403: OpenApiResponse(
                description="Only the owner may request a specific data import by PK"
            ),
            404: OpenApiResponse(description="Data import not found"),
        },
        tags=["importing"],
    )
    def get(self, request):
        """Return list or owner-only detail for data import ingestion status."""
        data_import_id = request.query_params.get("data_import_id")

        if not data_import_id:
            # Return list of DataImport objects the user can view
            permitted_qs = get_objects_for_user(
                request.user, "view_dataimport", klass=DataImport
            ).order_by("-date")
            serializer = DataImportUploadResponseSerializer(
                permitted_qs, many=True, context={"request": request}
            )
            return Response(serializer.data, status=status.HTTP_200_OK)

        # If a PK is provided, fetch the object and enforce owner-only access.
        try:
            data_import = DataImport.objects.get(pk=data_import_id)
        except DataImport.DoesNotExist:
            return Response(
                {"detail": "Data import not found."}, status=status.HTTP_404_NOT_FOUND
            )

        # Only the owner may request detailed info by PK
        if data_import.owner != request.user:
            return Response(
                {
                    "detail": "Only the owner may request this data import by primary key."  # noqa: E501
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # Owner may view full details (including log)
        serializer = DataImportDetailSerializer(
            data_import, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)
