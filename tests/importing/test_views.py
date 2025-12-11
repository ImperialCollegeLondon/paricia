from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from guardian.shortcuts import assign_perm, get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from formatting.models import Format
from importing.models import DataImport
from station.models import Station


class TestDataImportUploadAPIView(TestCase):
    """Test suite for the DataImportUploadAPIView."""

    fixtures = [
        "management_user",
        "variable_unit",
        "variable_variable",
        "station_country",
        "station_region",
        "station_ecosystem",
        "station_institution",
        "station_type",
        "station_place",
        "station_basin",
        "station_placebasin",
        "station_station",
        "formatting_delimiter",
        "formatting_extension",
        "formatting_date",
        "formatting_time",
        "formatting_format",
    ]

    def setUp(self):
        """Set up test data."""
        User = get_user_model()
        self.client = APIClient()

        # Create test users
        self.user_with_permission = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.user_without_permission = User.objects.create_user(
            username="otheruser", password="testpass123"
        )

        # Get station and format from fixtures
        self.station = Station.objects.get(pk=1)  # CAR_02_HC_01
        self.format = Format.objects.first()

        # Assign change_station permission to first user
        assign_perm("change_station", self.user_with_permission, self.station)

        # API endpoint URL
        self.url = reverse("importing:api_upload")

    def create_test_file(
        self, filename="test_data.csv", content=b"time,value\n2024-01-01,10.5\n"
    ):
        """Helper method to create a test file."""
        return SimpleUploadedFile(filename, content, content_type="text/csv")

    def test_authentication_required(self):
        """Test that authentication is required to access the endpoint."""
        test_file = self.create_test_file()

        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": test_file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_required_parameters(self):
        """Test that missing required parameters return 400 error."""
        self.client.force_authenticate(user=self.user_with_permission)

        # Missing all parameters
        response = self.client.post(self.url, {}, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Missing file
        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("rawfile", response.data)
        error_message = str(response.data["rawfile"][0]).lower()
        self.assertTrue("no file" in error_message or "required" in error_message)

        # Missing station
        test_file = self.create_test_file()
        response = self.client.post(
            self.url,
            {
                "format": self.format.pk,
                "rawfile": test_file,
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("station", response.data)

        # Missing format
        test_file = self.create_test_file()
        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "rawfile": test_file,
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("format", response.data)

    def test_invalid_station_code(self):
        """Test that invalid station code returns 400 error."""
        self.client.force_authenticate(user=self.user_with_permission)
        test_file = self.create_test_file()

        response = self.client.post(
            self.url,
            {
                "station": "INVALID_STATION",
                "format": self.format.pk,
                "rawfile": test_file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("station", response.data)
        error_message = str(response.data["station"][0]).lower()
        self.assertTrue("does not exist" in error_message or "invalid" in error_message)

    def test_invalid_format_id(self):
        """Test that invalid format ID returns 400 error."""
        self.client.force_authenticate(user=self.user_with_permission)
        test_file = self.create_test_file()

        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": 99999,  # Non-existent format ID
                "rawfile": test_file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("format", response.data)
        error_message = str(response.data["format"][0]).lower()
        self.assertTrue("does not exist" in error_message or "invalid" in error_message)

    def test_permission_denied(self):
        """Test that users without permission cannot upload data."""
        self.client.force_authenticate(user=self.user_without_permission)
        test_file = self.create_test_file()

        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": test_file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("permission", response.data["detail"].lower())

    def test_successful_upload(self):
        """Test successful file upload."""
        self.client.force_authenticate(user=self.user_with_permission)
        test_file = self.create_test_file()

        initial_count = DataImport.objects.count()

        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": test_file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(DataImport.objects.count(), initial_count + 1)

        # Check response structure
        self.assertIn("data_import_id", response.data)
        self.assertIn("station", response.data)
        self.assertIn("format", response.data)
        self.assertIn("rawfile", response.data)
        self.assertIn("date", response.data)
        self.assertIn("status", response.data)

        # Verify data
        self.assertEqual(response.data["station"], self.station.station_code)
        self.assertEqual(response.data["format"], self.format.pk)

    def test_successful_upload_with_optional_parameters(self):
        """Test successful file upload with optional parameters."""
        self.client.force_authenticate(user=self.user_with_permission)
        test_file = self.create_test_file()

        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": test_file,
                "visibility": "public",
                "reprocess": True,
                "observations": "Test upload with observations",
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Verify optional parameters were saved
        data_import = DataImport.objects.get(
            data_import_id=response.data["data_import_id"]
        )
        self.assertEqual(data_import.visibility, "public")
        self.assertTrue(data_import.reprocess)
        self.assertEqual(data_import.observations, "Test upload with observations")
        self.assertEqual(data_import.owner, self.user_with_permission)

    def test_visibility_choices(self):
        """Test that visibility parameter accepts valid choices."""
        self.client.force_authenticate(user=self.user_with_permission)

        # Test public visibility
        test_file = self.create_test_file()
        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": test_file,
                "visibility": "public",
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Test private visibility
        test_file = self.create_test_file()
        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": test_file,
                "visibility": "private",
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_invalid_visibility_choice(self):
        """Test that invalid visibility value returns 400 error."""
        self.client.force_authenticate(user=self.user_with_permission)
        test_file = self.create_test_file()

        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": test_file,
                "visibility": "invalid_choice",
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("visibility", response.data)
        error_message = str(response.data["visibility"][0]).lower()
        self.assertTrue(
            "invalid choice" in error_message or "not a valid choice" in error_message
        )

    def test_default_visibility(self):
        """Test that default visibility is 'private'."""
        self.client.force_authenticate(user=self.user_with_permission)
        test_file = self.create_test_file()

        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": test_file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data_import = DataImport.objects.get(
            data_import_id=response.data["data_import_id"]
        )
        self.assertEqual(data_import.visibility, "private")

    def test_default_reprocess(self):
        """Test that default reprocess is False."""
        self.client.force_authenticate(user=self.user_with_permission)
        test_file = self.create_test_file()

        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": test_file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data_import = DataImport.objects.get(
            data_import_id=response.data["data_import_id"]
        )
        self.assertFalse(data_import.reprocess)

    def test_file_types(self):
        """Test uploading different file types."""
        self.client.force_authenticate(user=self.user_with_permission)

        # CSV file
        csv_file = self.create_test_file("data.csv", b"time,value\n2024-01-01,10.5\n")
        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": csv_file,
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # TXT file
        txt_file = self.create_test_file("data.txt", b"time\tvalue\n2024-01-01\t10.5\n")
        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": txt_file,
            },
            format="multipart",
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_empty_observations(self):
        """Test that empty observations are handled correctly."""
        self.client.force_authenticate(user=self.user_with_permission)
        test_file = self.create_test_file()

        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": test_file,
                "observations": "",
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data_import = DataImport.objects.get(
            data_import_id=response.data["data_import_id"]
        )
        self.assertEqual(data_import.observations, "")

    def test_multiple_uploads_same_user(self):
        """Test that same user can upload multiple files."""
        self.client.force_authenticate(user=self.user_with_permission)

        # First upload
        test_file1 = self.create_test_file("data1.csv")
        response1 = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": test_file1,
            },
            format="multipart",
        )
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)

        # Second upload
        test_file2 = self.create_test_file("data2.csv")
        response2 = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": test_file2,
            },
            format="multipart",
        )
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        # Verify both imports exist and have different IDs
        self.assertNotEqual(
            response1.data["data_import_id"], response2.data["data_import_id"]
        )

    def test_owner_assignment(self):
        """Test that the upload is correctly assigned to the authenticated user."""
        self.client.force_authenticate(user=self.user_with_permission)
        test_file = self.create_test_file()

        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": test_file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data_import = DataImport.objects.get(
            data_import_id=response.data["data_import_id"]
        )
        self.assertEqual(data_import.owner, self.user_with_permission)

    def test_permission_for_different_stations(self):
        """Test that permissions are station-specific."""
        # Get another station from fixtures (without permission)
        other_station = Station.objects.exclude(pk=self.station.pk).first()

        self.client.force_authenticate(user=self.user_with_permission)
        test_file = self.create_test_file()

        # Try to upload to station without permission
        response = self.client.post(
            self.url,
            {
                "station": other_station.station_code,
                "format": self.format.pk,
                "rawfile": test_file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("permission", response.data["detail"].lower())

    def test_large_file_upload(self):
        """Test uploading a larger file."""
        self.client.force_authenticate(user=self.user_with_permission)

        # Create a larger file (1000 lines)
        content = b"time,value\n"
        for i in range(1000):
            content += f"2024-01-01 {i:02d}:00:00,{10.0 + i * 0.1}\n".encode()

        large_file = self.create_test_file("large_data.csv", content)

        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": large_file,
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_response_structure(self):
        """Test that response contains all expected fields."""
        self.client.force_authenticate(user=self.user_with_permission)
        test_file = self.create_test_file()

        response = self.client.post(
            self.url,
            {
                "station": self.station.station_code,
                "format": self.format.pk,
                "rawfile": test_file,
                "visibility": "public",
                "reprocess": True,
                "observations": "Test observations",
            },
            format="multipart",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check all expected fields are present
        expected_fields = [
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
            "reprocess",
        ]

        for field in expected_fields:
            self.assertIn(
                field, response.data, f"Field '{field}' missing from response"
            )
