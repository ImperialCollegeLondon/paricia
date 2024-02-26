from django.contrib.auth import get_user_model
from django.test import TestCase
from guardian.shortcuts import get_perms

from station.models import Station

User = get_user_model()


class StationPermissionsTest(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="password")
        self.user2 = User.objects.create_user(username="user2", password="password")
        self.station = Station.objects.create(owner=self.user1)

    def test_view_permission_for_all_users(self):
        self.assertTrue(self.user1.has_perm("station.view_station", self.station))
        self.assertTrue(self.user2.has_perm("station.view_station", self.station))

    def test_change_and_delete_permissions(self):
        self.assertTrue(self.user1.has_perm("station.change_station", self.station))
        self.assertTrue(self.user1.has_perm("station.delete_station", self.station))
        self.assertFalse(self.user2.has_perm("station.change_station", self.station))
        self.assertFalse(self.user2.has_perm("station.delete_station", self.station))
