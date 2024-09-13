from datetime import datetime

import pytz
from django.contrib.auth import get_user_model
from django.db.models.deletion import ProtectedError
from django.test import TestCase

from measurement.models import Measurement
from station.models import Country, Station
from variable.models import Variable

User = get_user_model()


class StationDeletionTest(TestCase):
    """Test deletion behaviour for the Station model."""

    def setUp(self):
        self.user_owner = User.objects.create_user(
            username="user_owner", password="password"
        )
        self.country = Country.objects.create(owner=self.user_owner)
        self.station = Station.objects.create(
            owner=self.user_owner, country=self.country
        )

    def test_delete_station(self):
        """Test that the station can be deleted."""
        self.station.delete()

    def test_delete_country(self):
        """Test for appropriate behavior when deleting the country."""
        # Country deletion should be forbidden while station exists
        with self.assertRaises(ProtectedError):
            self.country.delete()

        # Should be allowed after deleting the station
        self.station.delete()
        self.country.delete()

    def test_delete_owner(self):
        """Test for appropriate behavior when deleting the owner."""
        # Owner deletion should be forbidden while station exists
        with self.assertRaises(ProtectedError):
            self.user_owner.delete()

        # Should be allowed after deleting the station
        self.station.delete()
        self.user_owner.delete()


class MeasurementDeletionTest(TestCase):
    """Test deletion behaviour for the Measurement model."""

    def setUp(self):
        self.user_owner = User.objects.create_user(
            username="user_owner", password="password"
        )
        self.station = Station.objects.create(owner=self.user_owner)
        self.variable = Variable.objects.create(
            owner=self.user_owner, maximum=100, minimum=0
        )
        self.measurement = Measurement.objects.create(
            station=self.station,
            variable=self.variable,
            time=datetime(2018, 1, 9, 23, 55, 59, tzinfo=pytz.UTC),
            value=42,
        )

    def test_delete_measurement(self):
        """Test that the measurement can be deleted."""
        self.measurement.delete()

    def test_delete_station(self):
        """Test for appropriate behavior when deleting the station."""
        # Station deletion should be prevented while measurement exists
        with self.assertRaises(ProtectedError):
            self.station.delete()

        # Should be allowed after deleting the measurement
        self.measurement.delete()
        self.station.delete()

    def test_delete_variable(self):
        """Test for appropriate behavior when deleting the variable."""
        # Variable deletion should be prevented while measurement exists
        with self.assertRaises(ProtectedError):
            self.variable.delete()

        # Should be allowed after deleting the measurement
        self.measurement.delete()
        self.variable.delete()

    def test_delete_owner(self):
        """Test for appropriate behavior when deleting the owner."""
        # Owner deletion should be prevented while measurement exists
        with self.assertRaises(ProtectedError):
            self.user_owner.delete()

        # Should be allowed after deleting the measurement
        self.measurement.delete()
        self.user_owner.delete()

        # Station and variable should be deleted as well
        self.assertFalse(Station.objects.filter(pk=self.station.pk).exists())
        self.assertFalse(Variable.objects.filter(pk=self.variable.pk).exists())
