from datetime import datetime

import pytz
from django.test import TestCase
from model_bakery import baker


class TestModelCreation(TestCase):
    # TODO test creation from DataFrame
    # TODO test performance of creation and reading
    def setUp(self):
        from measurement.models import Flow, Precipitation

        flow1 = Flow.objects.create(
            station_id=1,
            time=datetime(2015, 10, 9, 23, 55, 59, tzinfo=pytz.UTC),
            average=10.2,
        )
        flow2 = Flow.objects.create(
            station_id=1,
            time=datetime(2016, 11, 9, 23, 55, 59, tzinfo=pytz.UTC),
            average=5.7,
        )
        precip1 = Precipitation.objects.create(
            station_id=2,
            time=datetime(2017, 12, 9, 23, 55, 59, tzinfo=pytz.UTC),
            sum=11.1,
        )
        precip2 = Precipitation.objects.create(
            station_id=2,
            time=datetime(2018, 1, 9, 23, 55, 59, tzinfo=pytz.UTC),
            sum=0.3,
        )

    def test_flow(self):
        from measurement.models import Flow

        flow_query = Flow.objects.get_queryset()
        self.assertEqual(len(flow_query), 2)

    def test_precipitation(self):
        from measurement.models import Precipitation

        precip_query = Precipitation.objects.get_queryset()
        self.assertEqual(len(precip_query), 2)

    def test_timescale_query(self):
        from measurement.models import Flow

        start_time, end_time = (
            datetime(2015, 1, 1, tzinfo=pytz.UTC),
            datetime(2016, 11, 10, tzinfo=pytz.UTC),
        )
        query = Flow.timescale.filter(time__range=[start_time, end_time], station_id=1)
        self.assertEqual(len(query), 2)

        end_time = datetime(2016, 11, 9, 23, 55, tzinfo=pytz.UTC)
        query = Flow.timescale.filter(time__range=[start_time, end_time], station_id=1)
        self.assertEqual(len(query), 1)

        query = Flow.timescale.filter(time__range=[start_time, end_time], station_id=2)
        self.assertEqual(len(query), 0)

    def test_query_ordering(self):
        from measurement.models import Precipitation

        query = Precipitation.timescale.filter(station_id=2).order_by("-time")
        self.assertEqual(query[0].time.year, 2018)
        self.assertEqual(query[1].time.year, 2017)


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
        )

    def test_clean(self):
        from measurement.models import ReportType

        # We check 'used_for_daily' compatibility
        # Works if report type is Hourly
        self.model.used_for_daily = True
        self.model.clean()

        # But fails for the other two
        self.model.report_type = ReportType.DAILY
        with self.assertRaises(ValueError):
            self.model.clean()

        self.model.report_type = ReportType.MONTLY
        with self.assertRaises(ValueError):
            self.model.clean()

        # We check 'used_for_monthly' compatibility
        # Works if report type is Daily
        self.model.used_for_daily = False
        self.model.used_for_monthly = True
        self.model.report_type = ReportType.DAILY
        self.model.clean()

        # But not for the other two
        self.model.report_type = ReportType.HOURLY
        with self.assertRaises(ValueError):
            self.model.clean()

        self.model.report_type = ReportType.MONTLY
        with self.assertRaises(ValueError):
            self.model.clean()


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
        with self.assertRaises(ValueError):
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
