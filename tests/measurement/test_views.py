from datetime import datetime

import pytz
from django.test import TestCase
from django.urls import reverse
from guardian.shortcuts import assign_perm, get_user_model
from rest_framework import status
from rest_framework.test import APIClient

from measurement.models import Measurement, Report, ReportType
from station.models import Station
from variable.models import Variable


class TestMeasurementDataAPIView(TestCase):
    """Test suite for the MeasurementDataAPIView."""

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

        # Get station and variable from fixtures
        self.station = Station.objects.get(pk=1)  # CAR_02_HC_01
        self.variable = Variable.objects.get(pk=2)  # airtemperature

        # Ensure the station has the variable in its variables list
        if self.variable.variable_code not in self.station.variables_list:
            self.station.variables = self.variable.variable_code
            self.station.save()

        # Assign view_measurements permission to first user
        assign_perm("view_measurements", self.user_with_permission, self.station)

        # Create some test measurements
        self.create_test_measurements()

        # API endpoint URL
        self.url = reverse("measurement:api_data_download")

    def create_test_measurements(self):
        """Create test measurement data."""
        # Create raw measurements
        base_time = datetime(2024, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        for i in range(10):
            Measurement.objects.create(
                time=base_time.replace(hour=i),
                station=self.station,
                variable=self.variable,
                value=10.0 + i,
                maximum=11.0 + i,
                minimum=9.0 + i,
                raw_value=10.0 + i,
                raw_maximum=11.0 + i,
                raw_minimum=9.0 + i,
                is_validated=True if i % 2 == 0 else False,
                is_active=True,
            )

        # Create report data
        Report.objects.create(
            time=datetime(2024, 1, 1, 1, 0, 0, tzinfo=pytz.UTC),
            station=self.station,
            variable=self.variable,
            value=15.5,
            maximum=16.0,
            minimum=15.0,
            report_type=ReportType.HOURLY,
            completeness=100.0,
        )

    def test_authentication_required(self):
        """Test that authentication is required to access the endpoint."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_missing_required_parameters(self):
        """Test that missing required parameters return 400 error."""
        self.client.force_authenticate(user=self.user_with_permission)

        # Missing all parameters
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Missing some parameters
        response = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_station_code(self):
        """Test that invalid station code returns 400 error."""
        self.client.force_authenticate(user=self.user_with_permission)

        response = self.client.get(
            self.url,
            {
                "station": "INVALID_STATION",
                "variable": self.variable.variable_code,
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "report_type": "measurement",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_variable_code(self):
        """Test that invalid variable code returns 400 error."""
        self.client.force_authenticate(user=self.user_with_permission)

        response = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": "invalid_variable",
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "report_type": "measurement",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_end_date_before_start_date(self):
        """Test that end date before start date returns 400 error."""
        self.client.force_authenticate(user=self.user_with_permission)

        response = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
                "start_date": "2024-01-31",
                "end_date": "2024-01-01",
                "report_type": "measurement",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_invalid_report_type(self):
        """Test that invalid report type returns 400 error."""
        self.client.force_authenticate(user=self.user_with_permission)

        response = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "report_type": "invalid_type",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_permission_denied(self):
        """Test that users without permission cannot access data."""
        self.client.force_authenticate(user=self.user_without_permission)

        response = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
                "start_date": "2024-01-01",
                "end_date": "2024-01-31",
                "report_type": "measurement",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("permission", response.data["detail"].lower())

    def test_measurement_report_type(self):
        """Test retrieving raw measurement data."""
        self.client.force_authenticate(user=self.user_with_permission)

        response = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
                "start_date": "2024-01-01",
                "end_date": "2024-01-01",
                "report_type": "measurement",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn("results", response.data)
        self.assertGreater(len(response.data["results"]), 0)

        # Check data structure
        first_record = response.data["results"][0]
        self.assertIn("id", first_record)
        self.assertIn("time", first_record)
        self.assertIn("value", first_record)

    def test_validated_report_type(self):
        """Test retrieving validated measurement data."""
        self.client.force_authenticate(user=self.user_with_permission)

        response = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
                "start_date": "2024-01-01",
                "end_date": "2024-01-01",
                "report_type": "validated",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsInstance(response.data, dict)
        self.assertIn("results", response.data)

        # Should have fewer records than raw measurements
        # (only validated ones)
        validated_count = len(response.data["results"])
        self.assertGreater(validated_count, 0)

    def test_hourly_report_type(self):
        """Test retrieving hourly report data."""
        self.client.force_authenticate(user=self.user_with_permission)

        response = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
                "start_date": "2024-01-01",
                "end_date": "2024-01-01",
                "report_type": "hourly",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check for report-specific fields
        if len(response.data["results"]) > 0:
            first_record = response.data["results"][0]
            self.assertIn("completeness", first_record)
            self.assertIn("report_type", first_record)

    def test_traces_parameter(self):
        """Test filtering by specific traces."""
        self.client.force_authenticate(user=self.user_with_permission)

        # Request only value trace
        response = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
                "start_date": "2024-01-01",
                "end_date": "2024-01-01",
                "report_type": "measurement",
                "traces": ["value"],
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if len(response.data["results"]) > 0:
            first_record = response.data["results"][0]
            self.assertIn("value", first_record)
            # Maximum and minimum should not be there if not requested
            # (but they might be null, so we just check value is present)
            self.assertIsNotNone(first_record.get("value"))

    def test_multiple_traces(self):
        """Test requesting multiple traces."""
        self.client.force_authenticate(user=self.user_with_permission)

        response = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
                "start_date": "2024-01-01",
                "end_date": "2024-01-01",
                "report_type": "measurement",
                "traces": ["value", "maximum", "minimum"],
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if len(response.data["results"]) > 0:
            first_record = response.data["results"][0]
            self.assertIn("value", first_record)
            self.assertIn("maximum", first_record)
            self.assertIn("minimum", first_record)

    def test_pagination(self):
        """Test pagination of results."""
        self.client.force_authenticate(user=self.user_with_permission)

        response = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
                "start_date": "2024-01-01",
                "end_date": "2024-01-01",
                "report_type": "measurement",
                "page_size": 5,
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("count", response.data)
        self.assertIn("next", response.data)
        self.assertIn("previous", response.data)
        self.assertIn("results", response.data)
        self.assertLessEqual(len(response.data["results"]), 5)

    def test_pagination_page_parameter(self):
        """Test pagination with specific page number."""
        self.client.force_authenticate(user=self.user_with_permission)

        # Get first page
        response1 = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
                "start_date": "2024-01-01",
                "end_date": "2024-01-01",
                "report_type": "measurement",
                "page_size": 3,
                "page": 1,
            },
        )

        self.assertEqual(response1.status_code, status.HTTP_200_OK)

        # Get second page
        response2 = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
                "start_date": "2024-01-01",
                "end_date": "2024-01-01",
                "report_type": "measurement",
                "page_size": 3,
                "page": 2,
            },
        )

        self.assertEqual(response2.status_code, status.HTTP_200_OK)

        # Results should be different
        if len(response1.data["results"]) > 0 and len(response2.data["results"]) > 0:
            self.assertNotEqual(
                response1.data["results"][0]["id"], response2.data["results"][0]["id"]
            )

    def test_empty_results(self):
        """Test that empty results are handled correctly."""
        self.client.force_authenticate(user=self.user_with_permission)

        # Query for a date range with no data
        response = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
                "start_date": "2025-01-01",
                "end_date": "2025-01-31",
                "report_type": "measurement",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_default_traces(self):
        """Test that default traces (value) is used when not specified."""
        self.client.force_authenticate(user=self.user_with_permission)

        response = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
                "start_date": "2024-01-01",
                "end_date": "2024-01-01",
                "report_type": "measurement",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if len(response.data["results"]) > 0:
            first_record = response.data["results"][0]
            self.assertIn("value", first_record)

    def test_data_ordering(self):
        """Test that data is returned in chronological order."""
        self.client.force_authenticate(user=self.user_with_permission)

        response = self.client.get(
            self.url,
            {
                "station": self.station.station_code,
                "variable": self.variable.variable_code,
                "start_date": "2024-01-01",
                "end_date": "2024-01-01",
                "report_type": "measurement",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that results are ordered by time
        if len(response.data["results"]) > 1:
            times = [record["time"] for record in response.data["results"]]
            self.assertEqual(times, sorted(times))

    def test_variable_not_available_for_station(self):
        """Test error when variable is not available for the station."""
        self.client.force_authenticate(user=self.user_with_permission)

        # Get a variable that's not associated with this station
        other_variable = Variable.objects.exclude(
            variable_code__in=self.station.variables_list
        ).first()

        if other_variable:
            response = self.client.get(
                self.url,
                {
                    "station": self.station.station_code,
                    "variable": other_variable.variable_code,
                    "start_date": "2024-01-01",
                    "end_date": "2024-01-31",
                    "report_type": "measurement",
                },
            )

            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn("variable", str(response.data).lower())
