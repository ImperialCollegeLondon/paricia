from datetime import datetime

import pytz
from django.test import TestCase


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

        start_time, end_time = datetime(2015, 1, 1, tzinfo=pytz.UTC), datetime(
            2016, 11, 10, tzinfo=pytz.UTC
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
