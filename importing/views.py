from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from guardian.shortcuts import get_objects_for_user
from rest_framework import status
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

    def get_permitted_stations(self, user):
        """Get stations the user has permission to import data for."""
        return get_objects_for_user(user, "change_station", klass=Station)

    @extend_schema(
        summary="Upload data file for import",
        description="""
        Upload a data file to create a new data import.

        **Permissions**: Users can only upload data for stations they have
        `change_station` permission for.

        **File Upload**: The file should be sent as multipart/form-data with
        the key `rawfile`.

        **Reprocess**: Set to `true` to reprocess the data after import.
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
                name="format",
                type=int,
                location=OpenApiParameter.QUERY,
                description="Format ID",
                required=True,
            ),
            OpenApiParameter(
                name="visibility",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Visibility level (public/private)",
                required=False,
                enum=["public", "private"],
            ),
            OpenApiParameter(
                name="reprocess",
                type=bool,
                location=OpenApiParameter.QUERY,
                description="Reprocess data after import",
                required=False,
            ),
            OpenApiParameter(
                name="observations",
                type=str,
                location=OpenApiParameter.QUERY,
                description="Additional observations",
                required=False,
            ),
        ],
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "rawfile": {
                        "type": "string",
                        "format": "binary",
                    }
                },
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
                            "id": 123,
                            "station": "H001",
                            "format": 1,
                            "rawfile": "/media/imports/data_2024.csv",
                            "visibility": "private",
                            "reprocess": True,
                            "created_at": "2024-12-09T10:30:00Z",
                            "status": "pending",
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
        tags=["data-import"],
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
                owner=request.user,  # Changed from 'user' to 'owner'
                # Note: date, start_date, end_date, records, status, and log
                # are set automatically by the model
            )
        except Exception as e:
            return Response(
                {"detail": f"Error creating data import: {e!s}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # Return the created import
        response_serializer = DataImportUploadResponseSerializer(data_import)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
