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

        self.period = 20
        self.start = datetime(2023, 1, 1, tzinfo=tz)
        self.end = datetime(2023, 2, 1, tzinfo=tz)
        self.date_range = pd.date_range(
            self.start, self.end, freq=f"{self.period}min", inclusive="left"
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
        obj = Measurement.objects.first()
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

    def test_flag_time_lapse_status(self):
        from measurement.validation import (
            TimeLapseStatus,
            flag_time_lapse_status,
            get_data_to_validate,
        )

        data = get_data_to_validate(
            station=self.station.station_code,
            variable=self.variable.variable_code,
            start_time=self.start.strftime("%Y-%m-%d"),
            end_time=self.end.strftime("%Y-%m-%d"),
        )

        time_lapse = flag_time_lapse_status(data, self.period)
        self.assertEqual(len(time_lapse), len(self.date_range))
        self.assertSetEqual(
            set(time_lapse.unique()),
            set([TimeLapseStatus.OK, TimeLapseStatus.NAN]),
        )

        period = self.period * 2
        time_lapse = flag_time_lapse_status(data, period)
        self.assertSetEqual(
            set(time_lapse.unique()),
            set([TimeLapseStatus.TOO_SMALL, TimeLapseStatus.NAN]),
        )

        period = self.period / 2
        time_lapse = flag_time_lapse_status(data, period)
        self.assertSetEqual(
            set(time_lapse.unique()),
            set([TimeLapseStatus.TOO_LARGE, TimeLapseStatus.NAN]),
        )

    def test_flag_value_status(self):
        from measurement.validation import (
            ValueStatus,
            flag_value_status,
            get_data_to_validate,
        )

        data = get_data_to_validate(
            station=self.station.station_code,
            variable=self.variable.variable_code,
            start_time=self.start.strftime("%Y-%m-%d"),
            end_time=self.end.strftime("%Y-%m-%d"),
        )

        # Allowed difference is large and possitive, so all values should be ok
        value_flag = flag_value_status(data, data.value.max() * 2)
        self.assertSetEqual(
            set(value_flag.unique()),
            set([ValueStatus.OK, ValueStatus.NAN]),
        )

        # Allowed difference is large and negative, so all values should be too large
        value_flag = flag_value_status(data, -data.value.max() * 2)
        self.assertSetEqual(
            set(value_flag.unique()),
            set([ValueStatus.TOO_LARGE, ValueStatus.NAN]),
        )

    def test_flag_value_limits(self):
        from measurement.validation import flag_value_limits

        data = pd.DataFrame(
            {
                "value": [1, 2, 3, 4, 5],
                "minimum": [0, 1, 2, 3, 4],
                "maximum": [2, 3, 4, 5, 6],
            }
        )
        maximum = 4
        minimum = 3
        svalue = (data.value.values < minimum) | (data.value.values > maximum)
        smax = (data.maximum.values < minimum) | (data.maximum.values > maximum)
        smin = (data.minimum.values < minimum) | (data.minimum.values > maximum)

        flags = flag_value_limits(data, maximum, minimum)
        assert len(flags.columns) == 3
        assert (flags.suspicius_value.values == svalue).all()
        assert (flags.suspicius_maximum.values == smax).all()
        assert (flags.suspicius_minimum.values == smin).all()
