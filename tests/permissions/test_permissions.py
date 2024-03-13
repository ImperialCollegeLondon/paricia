from django.contrib.auth import get_user_model
from django.test import TestCase
from guardian.shortcuts import get_anonymous_user

from sensor.models import Sensor
from station.models import Station, StationType
from variable.models import Variable

User = get_user_model()


class BasePermissionsTest:
    """Base class for testing object permissions."""

    @classmethod
    def setUpTestData(cls):
        """Create users for testing permissions."""
        cls.user_owner = User.objects.create_user(
            username="user_owner", password="password"
        )
        cls.user_other = User.objects.create_user(
            username="user_other", password="password"
        )
        cls.user_anon = get_anonymous_user()

        # The following must be set in the child classes
        cls.app = None
        cls.model = None
        cls.obj = None

    def _assert_perm(self, user, perm: str, obj, assert_true: bool):
        """
        Assert a single permission for a user against an object.

        Args:
            user: User to test permission for
            perm (str): Permission to test for (e.g. "change_station")
            obj: Object to test permission for
            assert_true (bool): Whether the permission should be True or False
        """

        if assert_true:
            self.assertTrue(user.has_perm(f"{self.app}.{perm}", obj))
        else:
            self.assertFalse(user.has_perm(f"{self.app}.{perm}", obj))

    def assert_perms(
        self,
        perm: str,
        obj,
        assert_owner: bool = None,
        assert_other: bool = None,
        assert_anon: bool = None,
    ):
        """Assert permissions for multiple users against an object.

        Args:
            perm (str): Permission to test for (e.g. "change_station")
            obj: Object to test permission for
            assert_owner (bool, optional): Whether the owner should have the permission.
            assert_other (bool, optional): Whether another user should have the
                permission.
            assert_anon (bool, optional): Whether the anonymous user should have the
                permission.
        """
        if assert_owner is not None:
            self._assert_perm(self.user_owner, perm, obj, assert_owner)
        if assert_other is not None:
            self._assert_perm(self.user_other, perm, obj, assert_other)
        if assert_anon is not None:
            self._assert_perm(self.user_anon, perm, obj, assert_anon)

    def test_change_permissions(self):
        """Test that only the owner can change the object."""
        self.assert_perms(f"change_{self.model}", self.obj, True, False, False)

    def test_delete_permissions(self):
        """Test that only the owner can delete the object."""
        self.assert_perms(f"delete_{self.model}", self.obj, True, False, False)

    def test_view_permissions(self):
        """Test that all users can view the object."""
        self.assert_perms(f"view_{self.model}", self.obj, True, True, True)


class StationTypePermissionsTest(BasePermissionsTest, TestCase):
    """Test permissions for StationType objects."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.app = "station"
        cls.model = "stationtype"
        cls.obj = StationType.objects.create(
            owner=cls.user_owner, permissions_level="public"
        )


class SensorPermissionsTest(BasePermissionsTest, TestCase):
    """Test permissions for Sensor objects."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.app = "sensor"
        cls.model = "sensor"
        cls.obj = Sensor.objects.create(
            owner=cls.user_owner, permissions_level="public"
        )


class VariablePermissionsTest(BasePermissionsTest, TestCase):
    """Test permissions for Variable objects."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.app = "variable"
        cls.model = "variable"
        cls.obj = Variable.objects.create(
            owner=cls.user_owner, maximum=100, minimum=0, permissions_level="public"
        )


class StationPermissionsTest(BasePermissionsTest, TestCase):
    """Test permissions for Station objects."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.app = "station"
        cls.model = "station"
        cls.station_private = Station.objects.create(
            owner=cls.user_owner, permissions_level="private"
        )
        cls.station_public = Station.objects.create(
            owner=cls.user_owner, permissions_level="public"
        )
        cls.station_internal = Station.objects.create(
            owner=cls.user_owner, permissions_level="internal"
        )
        cls.obj = cls.station_public

    def test_measurement_permissions_private(self):
        """Test that only the owner can view measurements for private stations."""
        self.assert_perms("view_measurements", self.station_private, True, False, False)

    def test_measurement_permissions_public(self):
        """Test that all users can view measurements for public stations."""
        self.assert_perms("view_measurements", self.station_public, True, True, True)

    def test_measurement_permissions_internal(self):
        """Test that only active users can view measurements for internal stations."""
        self.assert_perms("view_measurements", self.station_internal, True, True, False)
