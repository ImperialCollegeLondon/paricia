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
        cls.user_super = User.objects.create_superuser(
            username="user_super", password="password"
        )

        # The following must be set in the child classes
        cls.app = None
        cls.model = None
        cls.obj_private = None
        cls.obj_public = None

        # Internal objects are optional (applies to stations only)
        cls.obj_internal = None

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
        assert_super: bool = None,
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
            assert_super (bool, optional): Whether the superuser should have the
                permission.
        """
        if assert_owner is not None:
            self._assert_perm(self.user_owner, perm, obj, assert_owner)
        if assert_other is not None:
            self._assert_perm(self.user_other, perm, obj, assert_other)
        if assert_anon is not None:
            self._assert_perm(self.user_anon, perm, obj, assert_anon)
        if assert_super is not None:
            self._assert_perm(self.user_super, perm, obj, assert_super)

    def test_change_permissions(self):
        """Test that only the owner and superuser can change the objects."""
        self.assert_perms(
            f"change_{self.model}", self.obj_private, True, False, False, True
        )
        self.assert_perms(
            f"change_{self.model}", self.obj_public, True, False, False, True
        )
        if self.obj_internal:
            self.assert_perms(
                f"change_{self.model}", self.obj_internal, True, False, False, True
            )

    def test_delete_permissions(self):
        """Test that only the owner and superuser can delete the objects."""
        self.assert_perms(
            f"delete_{self.model}", self.obj_private, True, False, False, True
        )
        self.assert_perms(
            f"delete_{self.model}", self.obj_public, True, False, False, True
        )
        if self.obj_internal:
            self.assert_perms(
                f"delete_{self.model}", self.obj_internal, True, False, False, True
            )

    def test_view_permissions_private(self):
        """Test that only the owner and superuser can view private objects."""
        self.assert_perms(
            f"view_{self.model}", self.obj_private, True, False, False, True
        )

    def test_view_permissions_public(self):
        """Test that all users can view public objects."""
        self.assert_perms(f"view_{self.model}", self.obj_public, True, True, True, True)

    def test_view_permissions_internal(self):
        """Test that all users can view internal objects."""
        if self.obj_internal:
            self.assert_perms(
                f"view_{self.model}", self.obj_internal, True, True, True, True
            )


class StationTypePermissionsTest(BasePermissionsTest, TestCase):
    """Test permissions for StationType objects."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.app = "station"
        cls.model = "stationtype"
        cls.obj_private = StationType.objects.create(
            owner=cls.user_owner, permissions_level="private"
        )
        cls.obj_public = StationType.objects.create(
            owner=cls.user_owner, permissions_level="public"
        )


class SensorPermissionsTest(BasePermissionsTest, TestCase):
    """Test permissions for Sensor objects."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.app = "sensor"
        cls.model = "sensor"
        cls.obj_private = Sensor.objects.create(
            owner=cls.user_owner, permissions_level="private"
        )
        cls.obj_public = Sensor.objects.create(
            owner=cls.user_owner, permissions_level="public"
        )


class VariablePermissionsTest(BasePermissionsTest, TestCase):
    """Test permissions for Variable objects."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.app = "variable"
        cls.model = "variable"
        cls.obj_private = Variable.objects.create(
            owner=cls.user_owner, maximum=100, minimum=0, permissions_level="private"
        )
        cls.obj_public = Variable.objects.create(
            owner=cls.user_owner, maximum=100, minimum=0, permissions_level="public"
        )


class StationPermissionsTest(BasePermissionsTest, TestCase):
    """Test permissions for Station objects."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.app = "station"
        cls.model = "station"
        cls.obj_private = Station.objects.create(
            owner=cls.user_owner, permissions_level="private"
        )
        cls.obj_public = Station.objects.create(
            owner=cls.user_owner, permissions_level="public"
        )
        cls.obj_internal = Station.objects.create(
            owner=cls.user_owner, permissions_level="internal"
        )

    def test_measurement_permissions_private(self):
        """Test that only the owner and superuser can view measurements for private
        stations."""
        self.assert_perms(
            "view_measurements", self.obj_private, True, False, False, True
        )

    def test_measurement_permissions_public(self):
        """Test that all users can view measurements for public stations."""
        self.assert_perms("view_measurements", self.obj_public, True, True, True, True)

    def test_measurement_permissions_internal(self):
        """Test that only active users can view measurements for internal stations."""
        self.assert_perms(
            "view_measurements", self.obj_internal, True, True, False, True
        )


class StationPermissionsTestNewUser(StationPermissionsTest):
    """Test Station permissions for a new user."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.user_other = User.objects.create_user(
            username="user_other_new", password="password"
        )


class StationPermissionsTestChangePermissions(StationPermissionsTest):
    """Test changing permissions level for Station objects."""

    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()

        # Change the permissions level for the stations
        cls.obj_private.permissions_level = "public"
        cls.obj_public.permissions_level = "internal"
        cls.obj_internal.permissions_level = "private"
        cls.obj_private.save()
        cls.obj_public.save()
        cls.obj_internal.save()

        # Swap the stations for the tests
        cls.obj_private, cls.obj_public, cls.obj_internal = (
            cls.obj_internal,
            cls.obj_private,
            cls.obj_public,
        )