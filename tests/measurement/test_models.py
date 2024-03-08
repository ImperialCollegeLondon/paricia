from datetime import datetime

import pytz
from django.core.exceptions import ValidationError
from django.test import TestCase
from model_bakery import baker


class TestReport(TestCase):
    def setUp(self) -> None:
        from measurement.models import Report, ReportType
        from station.models import Station
        from variable.models import Variable

        station = baker.make(Station)
        variable = baker.make(Variable)
        self.model: Report = Report(
            time=datetime(2018, 1, 9, 23, 55, 59, tzinfo=pytz.UTC),
            station=station,
            variable=variable,
            value=42,
            report_type=ReportType.HOURLY,
            completeness=1,
        )

    def test_clean_time_hourly(self):
        from measurement.models import ReportType

        self.model.report_type = ReportType.HOURLY
        self.model.clean()
        expected_time = datetime(2018, 1, 9, 23, 0, 0, tzinfo=pytz.UTC)
        self.assertEqual(self.model.time, expected_time)

    def test_clean_time_daily(self):
        from measurement.models import ReportType

        self.model.report_type = ReportType.DAILY
        self.model.clean()
        expected_time = datetime(2018, 1, 9, 0, 0, 0, tzinfo=pytz.UTC)
        self.assertEqual(self.model.time, expected_time)

    def test_clean_time_monthly(self):
        from measurement.models import ReportType

        self.model.report_type = ReportType.MONTLY
        self.model.clean()
        expected_time = datetime(2018, 1, 1, 0, 0, 0, tzinfo=pytz.UTC)
        self.assertEqual(self.model.time, expected_time)


class TestMeasurement(TestCase):
    def setUp(self) -> None:
        from measurement.models import Measurement
        from station.models import Station
        from variable.models import Variable

        station = baker.make(Station)
        variable = baker.make(Variable)
        self.model: Measurement = Measurement(
            time=datetime(2018, 1, 9, 23, 55, 59, tzinfo=pytz.UTC),
            station=station,
            variable=variable,
            value=42,
        )

    def test_clean_backup_raws(self):
        # Initially, there's no raw
        self.assertIsNone(self.model.raw_value)

        # But after running clean, there is and is equal to value
        self.model.clean()
        self.assertEqual(self.model.value, self.model.raw_value)

    def test_clean_validation(self):
        # When not validated and active, all should be ok
        self.model.clean()

        # If becomes inactive but is not validated, there's an error
        self.model.is_validated = False
        self.model.is_active = False
        with self.assertRaises(ValidationError):
            self.model.clean()

        # If it is inactive but has been validated, then it is ok again
        self.model.is_validated = True
        self.model.is_active = False
        self.model.clean()

    def test_overwritten(self):
        # If we start fresh, it is not overwritten
        self.model.clean()
        self.assertFalse(self.model.overwritten)

        # But if we change it, it should be overwritten
        self.model.value = 32
        self.assertTrue(self.model.overwritten)
