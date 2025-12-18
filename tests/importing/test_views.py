from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse
from guardian.shortcuts import assign_perm, get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from formatting.models import Format
from importing.models import DataImport
from station.models import Station

IMPORTING_TEST_FIXTURES = [
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


class TestDataImportUploadAPIView(TestCase):
    """Test suite for the DataImportUploadAPIView."""

    fixtures = IMPORTING_TEST_FIXTURES

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
        self.assertIn("status_display", response.data)

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
            "status_display",
            "reprocess",
        ]

        for field in expected_fields:
            self.assertIn(
                field, response.data, f"Field '{field}' missing from response"
            )


class TestDataIngestionQueryView(TestCase):
    """Test suite for the DataingestionQueryView."""

    fixtures = IMPORTING_TEST_FIXTURES

    def setUp(self):
        """Set up test data."""
        User = get_user_model()
        self.client = APIClient()

        # Create test users
        self.owner_user = User.objects.create_user(
            username="owner", password="testpass123"
        )
        self.other_user = User.objects.create_user(
            username="otheruser", password="testpass123"
        )
        self.third_user = User.objects.create_user(
            username="thirduser", password="testpass123"
        )

        # Get station and format from fixtures
        self.station = Station.objects.get(pk=1)
        self.format = Format.objects.first()

        # Create test data imports
        # Owner's import (completed successfully)
        self.owner_import = DataImport.objects.create(
            station=self.station,
            format=self.format,
            rawfile=SimpleUploadedFile(
                "owner_data.csv", b"time,value\n2024-01-01,10.5\n"
            ),
            owner=self.owner_user,
            visibility="private",
            status="C",
            log="Data ingestion completed successfully",
            records=100,
        )

        # Owner's failed import
        self.owner_failed_import = DataImport.objects.create(
            station=self.station,
            format=self.format,
            rawfile=SimpleUploadedFile("owner_failed.csv", b"invalid data"),
            owner=self.owner_user,
            visibility="private",
            status="F",
            log="Error: Invalid data format at line 5",
            records=0,
        )

        # Other user's import
        self.other_import = DataImport.objects.create(
            station=self.station,
            format=self.format,
            rawfile=SimpleUploadedFile(
                "other_data.csv", b"time,value\n2024-01-02,20.5\n"
            ),
            owner=self.other_user,
            visibility="private",
            status="N",
            log="",
        )

        # Public import from other user
        self.public_import = DataImport.objects.create(
            station=self.station,
            format=self.format,
            rawfile=SimpleUploadedFile(
                "public_data.csv", b"time,value\n2024-01-03,30.5\n"
            ),
            owner=self.other_user,
            visibility="public",
            status="C",
            log="Public import completed",
            records=50,
        )

        # Set object permissions (mimicking PermissionsBase behavior)
        assign_perm("view_dataimport", self.owner_user, self.owner_import)
        assign_perm("view_dataimport", self.owner_user, self.owner_failed_import)
        assign_perm("view_dataimport", self.other_user, self.other_import)
        # Public imports are viewable by all
        assign_perm("view_dataimport", self.owner_user, self.public_import)
        assign_perm("view_dataimport", self.other_user, self.public_import)
        assign_perm("view_dataimport", self.third_user, self.public_import)

        # API endpoint URL
        self.url = reverse("importing:api_data_ingestion")

    def test_authentication_required(self):
        """Test that authentication is required to access the endpoint."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_returns_only_viewable_imports(self):
        """Test that list only returns imports the user has permission to view."""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, list)

        # Should see own imports and public import
        returned_ids = {item["data_import_id"] for item in response.data}
        self.assertIn(self.owner_import.data_import_id, returned_ids)
        self.assertIn(self.owner_failed_import.data_import_id, returned_ids)
        self.assertIn(self.public_import.data_import_id, returned_ids)
        # Should NOT see other user's private import
        self.assertNotIn(self.other_import.data_import_id, returned_ids)

    def test_list_contains_expected_fields(self):
        """Test that list items contain expected fields but not log."""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

        first_item = response.data[0]
        expected_fields = [
            "data_import_id",
            "station",
            "format",
            "date",
            "status_display",
        ]
        for field in expected_fields:
            self.assertIn(field, first_item)

        # Log should NOT be in list response
        self.assertNotIn("log", first_item)

    def test_empty_list_for_user_without_permissions(self):
        """Test that user with no permissions sees empty list."""
        self.client.force_authenticate(user=self.third_user)
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Should only see public import
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["data_import_id"], self.public_import.data_import_id
        )

    def test_detail_owner_can_view(self):
        """Test that owner can view their own import detail including log."""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(
            self.url, {"data_import_id": self.owner_import.data_import_id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["data_import_id"], self.owner_import.data_import_id
        )
        self.assertIn("log", response.data)
        self.assertEqual(response.data["log"], "Data ingestion completed successfully")
        self.assertEqual(response.data["status"], "C")
        self.assertEqual(response.data["status_display"], "Completed")

    def test_detail_owner_can_view_failed_import_with_log(self):
        """Test that owner can see error log for failed imports."""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(
            self.url, {"data_import_id": self.owner_failed_import.data_import_id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data["data_import_id"], self.owner_failed_import.data_import_id
        )
        self.assertIn("log", response.data)
        self.assertEqual(response.data["log"], "Error: Invalid data format at line 5")
        self.assertEqual(response.data["status"], "F")
        self.assertEqual(response.data["status_display"], "Failed")

    def test_detail_non_owner_forbidden(self):
        """Test that non-owner cannot view detail even with view permission."""
        # Give other_user view permission on owner's import
        assign_perm("view_dataimport", self.other_user, self.owner_import)

        self.client.force_authenticate(user=self.other_user)
        response = self.client.get(
            self.url, {"data_import_id": self.owner_import.data_import_id}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("owner", response.data["detail"].lower())

    def test_detail_public_import_non_owner_forbidden(self):
        """Test that non-owner cannot view detail of public import by PK."""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(
            self.url, {"data_import_id": self.public_import.data_import_id}
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_detail_nonexistent_import(self):
        """Test requesting detail for non-existent import returns 404."""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(self.url, {"data_import_id": 99999})

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("not found", response.data["detail"].lower())

    def test_detail_response_contains_all_fields(self):
        """Test that detail response contains all expected fields including log."""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(
            self.url, {"data_import_id": self.owner_import.data_import_id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

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
            "status_display",
            "reprocess",
            "log",
        ]

        for field in expected_fields:
            self.assertIn(
                field, response.data, f"Field '{field}' missing from detail response"
            )

    def test_detail_rawfile_is_absolute_url(self):
        """Test that rawfile field returns absolute URL in detail response."""
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(
            self.url, {"data_import_id": self.owner_import.data_import_id}
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("rawfile", response.data)
        # Should be a full URL starting with http
        rawfile_url = response.data["rawfile"]
        self.assertTrue(
            rawfile_url.startswith("http://") or rawfile_url.startswith("https://"),
            f"rawfile should be absolute URL, got: {rawfile_url}",
        )

    def test_status_display_field(self):
        """Test that status_display returns human-readable status."""
        self.client.force_authenticate(user=self.owner_user)

        # Test completed status
        response = self.client.get(
            self.url, {"data_import_id": self.owner_import.data_import_id}
        )
        self.assertEqual(response.data["status"], "C")
        self.assertEqual(response.data["status_display"], "Completed")

        # Test failed status
        response = self.client.get(
            self.url, {"data_import_id": self.owner_failed_import.data_import_id}
        )
        self.assertEqual(response.data["status"], "F")
        self.assertEqual(response.data["status_display"], "Failed")

    def test_list_and_detail_use_station_code(self):
        """Test that station is returned as station_code (slug) not ID."""
        self.client.force_authenticate(user=self.owner_user)

        # Test list
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_item = response.data[0]
        self.assertEqual(first_item["station"], self.station.station_code)

        # Test detail
        response = self.client.get(
            self.url, {"data_import_id": self.owner_import.data_import_id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["station"], self.station.station_code)

    def test_detail_access_control_strictly_by_ownership(self):
        """Test that detail access is strictly controlled by ownership."""
        # Create a new import
        special_import = DataImport.objects.create(
            station=self.station,
            format=self.format,
            rawfile=SimpleUploadedFile("special.csv", b"data"),
            owner=self.owner_user,
            visibility="public",
            status="C",
            log="Special import log",
        )

        # Give third_user explicit view permission
        assign_perm("view_dataimport", self.third_user, special_import)
        assign_perm("change_dataimport", self.third_user, special_import)

        # Even with view and change permissions, non-owner cannot access detail by PK
        self.client.force_authenticate(user=self.third_user)
        response = self.client.get(
            self.url, {"data_import_id": special_import.data_import_id}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # But owner can
        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get(
            self.url, {"data_import_id": special_import.data_import_id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("log", response.data)
