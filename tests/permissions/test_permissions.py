from django.contrib.auth import get_user_model
from django.test import TestCase

from sensor.models import Sensor
from station.models import Station, StationType

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
        cls.app = ""

    def _assert_perm(self, user, perm, obj, assert_true):
        """Helper function to assert single permission."""
        if assert_true:
            self.assertTrue(user.has_perm(f"{self.app}.{perm}", obj))
        else:
            self.assertFalse(user.has_perm(f"{self.app}.{perm}", obj))

    def _assert_perms(
        self,
        perm,
        obj,
        assert_owner=None,
        assert_other=None,
        assert_inactive=None,
    ):
        """Helper function to assert multiple permissions."""
        if assert_owner:
            self._assert_perm(self.user_owner, perm, obj, assert_owner)
        if assert_other:
            self._assert_perm(self.user_other, perm, obj, assert_other)
        if assert_inactive:
            self._assert_perm(self.user_inactive, perm, obj, assert_inactive)


class StationTypePermissionsTest(BasePermissionsTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.app = "station"
        cls.station_type = StationType.objects.create(owner=cls.user_owner)

    def test_change_permissions(self):
        """Test that only the owner can change the station type."""
        self._assert_perms("change_stationtype", self.station_type, True, False, False)

    def test_delete_permissions(self):
        """Test that only the owner can delete the station type."""
        self._assert_perms("delete_stationtype", self.station_type, True, False, False)

    def test_view_permissions(self):
        """Test that all users can view the station type."""
        self._assert_perms("view_stationtype", self.station_type, True, True, True)


class SensorPermissionsTest(BasePermissionsTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.app = "sensor"
        cls.sensor = Sensor.objects.create(owner=cls.user_owner)

    def test_change_permissions(self):
        """Test that only the owner can change the sensor."""
        self._assert_perms("change_sensor", self.sensor, True, False, False)

    def test_delete_permissions(self):
        """Test that only the owner can delete the sensor."""
        self._assert_perms("delete_sensor", self.sensor, True, False, False)

    def test_view_permissions(self):
        """Test that all users can view the sensor."""
        self._assert_perms("view_sensor", self.sensor, True, True, True)


class StationPermissionsTest(BasePermissionsTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.app = "station"
        cls.station_private = Station.objects.create(
            owner=cls.user_owner, permissions_level="private"
        )
        cls.station_public = Station.objects.create(
            owner=cls.user_owner, permissions_level="public"
        )
        cls.station_internal = Station.objects.create(
            owner=cls.user_owner, permissions_level="internal"
        )

    def test_change_permissions(self):
        """Test that only the owner can change the stations."""
        self._assert_perms("change_station", self.station_public, True, False, False)

    def test_delete_permissions(self):
        """Test that only the owner can delete the stations."""
        self._assert_perms("delete_station", self.station_public, True, False, False)

    def test_view_permissions(self):
        """Test that all users can view the stations."""
        self._assert_perms("view_station", self.station_public, True, True, True)

    def test_measurement_permissions_private(self):
        """Test that only the owner can view measurements for private stations."""
        self._assert_perms(
            "view_measurements", self.station_private, True, False, False
        )

    def test_measurement_permissions_public(self):
        """Test that all users can view measurements for public stations."""
        self._assert_perms("view_measurements", self.station_public, True, True, True)

    def test_measurement_permissions_internal(self):
        """Test that only active users can view measurements for internal stations."""
        self._assert_perms(
            "view_measurements", self.station_internal, True, True, False
        )
