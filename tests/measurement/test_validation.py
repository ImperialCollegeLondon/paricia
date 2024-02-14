import random
import zoneinfo
from datetime import datetime
from decimal import Decimal

import pandas as pd
from django.test import TestCase
from model_bakery import baker


class TestValidationFunctions(TestCase):
    def setUp(self):
        from measurement.models import Measurement
        from station.models import Station
        from variable.models import Variable

        self.station = baker.make(Station)
        self.variable = baker.make(Variable)

        if self.station.timezone is None:
            self.station.timezone = "UTC"
            self.station.save()
        tz = zoneinfo.ZoneInfo(self.station.timezone)

        self.start = datetime(2023, 1, 1, tzinfo=tz)
        self.end = datetime(2023, 2, 1, tzinfo=tz)
        self.date_range = pd.date_range(
            self.start, self.end, freq="20min", inclusive="left"
        )

        minimum = random.randint(-5, 5)
        maximum = random.randint(20, 30)
        records = [
            Measurement(
                station=self.station,
                variable=self.variable,
                time=t,
                value=Decimal(random.randint(minimum, maximum)),
                minimum=Decimal(minimum),
                maximum=Decimal(maximum),
            )
            for t in self.date_range
        ]

        [r.clean() for r in records]  # type: ignore
        Measurement.objects.bulk_create(records)

    def test_get_data_to_validate(self):
        from measurement.models import Measurement
        from measurement.validation import get_data_to_validate

        # Make one data point already validated
        obj = Measurement.objects.get(id=1)
        obj.is_validated = True
        obj.clean()
        obj.save()

        # This should return one less than the length of the date range
        data = get_data_to_validate(
            station=self.station.station_code,
            variable=self.variable.variable_code,
            start_time=self.start.strftime("%Y-%m-%d"),
            end_time=self.end.strftime("%Y-%m-%d"),
        )
        self.assertEqual(len(data), len(self.date_range) - 1)

        # The validated object should not be in the data
        self.assertNotIn(obj.id, data.id.values)
