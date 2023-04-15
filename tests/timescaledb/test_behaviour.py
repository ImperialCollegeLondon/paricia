from datetime import datetime

import pytz
from django.test import TestCase


class TestTimescaleDB(TestCase):
    # TODO test creation from DataFrame
    # TODO test performance of creation and reading
    def setUp(self):
        from measurement.models import Flow

        flow1 = Flow.objects.create(
            station_id=1,
            time=datetime(2015, 10, 9, 23, 55, 59, tzinfo=pytz.UTC),
            value=10.2,
        )
        flow2 = Flow.objects.create(
            station_id=1,
            time=datetime(2015, 10, 9, 23, 55, 59, tzinfo=pytz.UTC),
            value=10.2,
        )
