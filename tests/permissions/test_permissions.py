from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.test import TestCase

from measurement.models import Measurement
from sensor.models import Sensor
from station.models import Station, StationType
from variable.models import Variable

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
        cls.model = ""

    def _assert_perm(self, user, perm, obj, assert_true):
        """Helper function to assert single permission."""
        if assert_true:
            self.assertTrue(user.has_perm(f"{self.app}.{perm}_{self.model}", obj))
        else:
            self.assertFalse(user.has_perm(f"{self.app}].{perm}_{self.model}", obj))

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
        cls.model = "stationtype"
        cls.station_type = StationType.objects.create(owner=cls.user_owner)

    def test_change_permissions(self):
        """Test that only the owner can change the station type."""
        self._assert_perms("change", self.station_type, True, False, False)

    def test_delete_permissions(self):
        """Test that only the owner can delete the station type."""
        self._assert_perms("delete", self.station_type, True, False, False)

    def test_view_permissions(self):
        """Test that all users can view the station type."""
        self._assert_perms("view", self.station_type, True, True, True)


class StationPermissionsTest(BasePermissionsTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.app = "station"
        cls.model = "station"
        cls.station = Station.objects.create(owner=cls.user_owner)

    def test_change_permissions(self):
        """Test that only the owner can change the station."""
        self._assert_perms("change", self.station, True, False, False)

    def test_delete_permissions(self):
        """Test that only the owner can delete the station."""
        self._assert_perms("delete", self.station, True, False, False)

    def test_view_permissions(self):
        """Test that all users can view the station."""
        self._assert_perms("view", self.station, True, True, True)


class SensorPermissionsTest(BasePermissionsTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.app = "sensor"
        cls.model = "sensor"
        cls.sensor = Sensor.objects.create(owner=cls.user_owner)

    def test_change_permissions(self):
        """Test that only the owner can change the sensor."""
        self._assert_perms("change", self.sensor, True, False, False)

    def test_delete_permissions(self):
        """Test that only the owner can delete the sensor."""
        self._assert_perms("delete", self.sensor, True, False, False)

    def test_view_permissions(self):
        """Test that all users can view the sensor."""
        self._assert_perms("view", self.sensor, True, True, True)


class MeasurementPermissionsTest(BasePermissionsTest):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.app = "measurement"
        cls.model = "measurement"
        cls.station_private = Station.objects.create(
            owner=cls.user_owner, permissions_level="private"
        )
        cls.station_public = Station.objects.create(
            owner=cls.user_owner, permissions_level="public"
        )
        cls.station_internal = Station.objects.create(
            owner=cls.user_owner, permissions_level="internal"
        )
        time = datetime(2024, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        variable = Variable.objects.create(name="test", maximum=2, minimum=0)
        cls.meas_private = Measurement.objects.create(
            station=cls.station_private,
            time=time,
            value=1,
            variable=variable,
        )
        cls.meas_public = Measurement.objects.create(
            station=cls.station_public,
            time=time,
            value=1,
            variable=variable,
        )
        cls.meas_internal = Measurement.objects.create(
            station=cls.station_internal,
            time=time,
            value=1,
            variable=variable,
        )

    def test_change_permissions(self):
        """Test that only the owner can change the measurement."""
        self._assert_perms("change", self.meas_private, True, False, False)

    def test_delete_permissions(self):
        """Test that only the owner can delete the measurement."""
        self._assert_perms("delete", self.meas_private, True, False, False)

    def test_view_permissions_private(self):
        """Test that only the owner can view the private measurement."""
        self._assert_perms("view", self.meas_private, True, False, False)

    def test_view_permissions_internal(self):
        """Test that only active users can view the internal measurement."""
        self._assert_perms("view", self.meas_internal, True, True, False)

    def test_view_permissions_public(self):
        """Test that all users can view the public measurement."""
        self._assert_perms("view", self.meas_public, True, True, True)