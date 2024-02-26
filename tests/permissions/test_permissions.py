from django.contrib.auth import get_user_model
from django.test import TestCase

from measurement.models import Measurement
from station.models import Station

User = get_user_model()


class BasePermissionsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user_owner = User.objects.create_user(
            username="user_owner", password="password"
        )
        cls.user_other = User.objects.create_user(
            username="user_other", password="password"
        )
        cls.user_inactive = User.objects.create_user(
            username="user_inactive", password="password", is_active=False
        )


class StationPermissionsTest(BasePermissionsTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.station = Station.objects.create(owner=cls.user_owner)

    def test_change_permissions(self):
        """Test that only the owner can change the station."""
        self.assert_perm(self.user_owner, "change", self.station, True)
        self.assert_perm(self.user_other, "change", self.station, False)
        self.assert_perm(self.user_inactive, "change", self.station, False)

    def test_delete_permissions(self):
        """Test that only the owner can delete the station."""
        self.assert_perm(self.user_owner, "delete", self.station, True)
        self.assert_perm(self.user_other, "delete", self.station, False)
        self.assert_perm(self.user_inactive, "delete", self.station, False)

    def test_view_permissions(self):
        """Test that all users can view the station."""
        self.assert_perm(self.user_owner, "view", self.station, True)
        self.assert_perm(self.user_other, "view", self.station, True)
        self.assert_perm(self.user_inactive, "view", self.station, True)

    def assert_perm(self, user, perm, obj, expected):
        """Helper function to assert permissions."""
        if expected:
            self.assertTrue(user.has_perm(f"station.{perm}_station", obj))
        else:
            self.assertFalse(user.has_perm(f"station.{perm}_station", obj))


class MeasurementPermissionsTest(BasePermissionsTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.station_private = Station.objects.create(
            owner=cls.user_owner, permissions_level="private"
        )
        cls.station_public = Station.objects.create(
            owner=cls.user_owner, permissions_level="public"
        )
        cls.station_internal = Station.objects.create(
            owner=cls.user_owner, permissions_level="internal"
        )
        cls.meas_private = Measurement.objects.create(station=cls.station_private)
        cls.meas_public = Measurement.objects.create(station=cls.station_public)
        cls.meas_internal = Measurement.objects.create(station=cls.station_internal)

    def test_change_permissions(self):
        """Test that only the owner can change the measurement."""
        self.assert_perm(self.user_owner, "change", self.meas_private, True)
        self.assert_perm(self.user_other, "change", self.meas_private, False)
        self.assert_perm(self.user_inactive, "change", self.meas_internal, False)

    def test_delete_permissions(self):
        """Test that only the owner can delete the measurement."""
        self.assert_perm(self.user_owner, "delete", self.meas_private, True)
        self.assert_perm(self.user_other, "delete", self.meas_private, False)
        self.assert_perm(self.user_inactive, "delete", self.meas_internal, False)

    def test_view_permissions_private(self):
        """Test that only the owner can view the private measurement."""
        self.assert_perm(self.user_owner, "view", self.meas_private, True)
        self.assert_perm(self.user_other, "view", self.meas_private, False)
        self.assert_perm(self.user_inactive, "view", self.meas_private, False)

    def test_view_permissions_internal(self):
        """Test that only active users can view the internal measurement."""
        self.assert_perm(self.user_owner, "view", self.meas_internal, True)
        self.assert_perm(self.user_other, "view", self.meas_internal, True)
        self.assert_perm(self.user_inactive, "view", self.meas_internal, False)

    def test_view_permissions_public(self):
        """Test that all users can view the public measurement."""
        self.assert_perm(self.user_owner, "view", self.meas_public, True)
        self.assert_perm(self.user_other, "view", self.meas_public, True)
        self.assert_perm(self.user_inactive, "view", self.meas_public, True)

    def assert_perm(self, user, perm, obj, expected):
        """Helper function to assert permissions."""
        if expected:
            self.assertTrue(user.has_perm(f"measurement.{perm}_measurement", obj))
        else:
            self.assertFalse(user.has_perm(f"measurement.{perm}_measurement", obj))
