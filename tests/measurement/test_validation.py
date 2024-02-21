import random
import zoneinfo
from datetime import datetime
from decimal import Decimal

import numpy as np
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

        # This should return the full date range, including the validated object
        data = get_data_to_validate(
            station=self.station.station_code,
            variable=self.variable.variable_code,
            start_time=self.start.strftime("%Y-%m-%d"),
            end_time=self.end.strftime("%Y-%m-%d"),
            include_validated=True,
        )
        self.assertEqual(len(data), len(self.date_range))

        # The validated object should be in the data
        self.assertIn(obj.id, data.id.values)

    def test_flag_time_lapse_status(self):
        from measurement.validation import flag_time_lapse_status

        period = 5
        times = pd.date_range(
            "2023-01-01", "2023-01-2", freq=f"{period}min"
        ).to_series()
        times.iloc[3] = times.iloc[3] + pd.Timedelta("1min")
        times.iloc[10] = times.iloc[10] + pd.Timedelta("1min")
        data = pd.DataFrame({"time": times})
        expected = times.diff() != pd.Timedelta(f"{period}min")
        expected.iloc[0] = False
        time_lapse = flag_time_lapse_status(data, period)
        assert (time_lapse.suspicius_time_lapse.values == expected).all()

    def test_flag_value_status(self):
        from measurement.validation import flag_value_difference

        data = pd.DataFrame({"value": [1, 3, 5, 6, 6]})
        allowed_difference = 1.5
        expected = data.value.diff().abs().values > allowed_difference
        expected[0] = False
        flags = flag_value_difference(data, allowed_difference)
        assert (flags.suspicius_value_difference.values == expected).all()

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
        assert (flags.suspicius_value_limits.values == svalue).all()
        assert (flags.suspicius_maximum_limits.values == smax).all()
        assert (flags.suspicius_minimum_limits.values == smin).all()

    def test_find_suspicious_data(self):
        from measurement.validation import flag_suspicius_data

        # Create a sample dataframe
        time = pd.date_range("2023-01-01", "2023-01-02", freq="5min")
        data = pd.DataFrame(
            {
                "time": time,
                "value": np.arange(len(time)),
                "minimum": np.arange(len(time)),
                "maximum": np.arange(len(time)),
            }
        )

        maximum = Decimal(4)
        minimum = Decimal(3)
        period = Decimal(5)
        allowed_difference = Decimal(1.5)

        # Call the function under test
        result = flag_suspicius_data(data, maximum, minimum, period, allowed_difference)

        # Assert the expected output
        expected_columns = [
            "suspicius_time_lapse",
            "suspicius_value_difference",
            "suspicius_value_limits",
            "suspicius_maximum_limits",
            "suspicius_minimum_limits",
        ]
        self.assertListEqual(list(result.columns), expected_columns)
        self.assertEqual(len(result), len(data))

    def test_generate_daily_report(self):
        from measurement.validation import generate_daily_report

        time = pd.date_range("2023-01-01", "2023-01-02", periods=5)

        # Create sample data
        data = pd.DataFrame(
            {
                "time": time,
                "value": [1.0, 2.0, 3.0, 4.0, 5.0],
                "maximum": [2.0, 3.0, 4.0, 5.0, 6.0],
                "minimum": [0.0, 1.0, 2.0, 3.0, 4.0],
            }
        )
        suspicius = pd.DataFrame(
            {
                "suspicius_value_limits": [0, 1, 0, 1, 0],
                "suspicius_maximum_limits": [0, 0, 1, 0, 1],
                "suspicius_minimum_limits": [1, 0, 0, 1, 0],
            }
        ).astype(int)

        # Call the function under test using 'sum' as operation
        operation = "sum"
        result = generate_daily_report(data, suspicius, operation)

        # Assert the expected output
        expected = pd.DataFrame(
            {
                "value": [10.0, 5.0],
                "maximum": [5.0, 6.0],
                "minimum": [0.0, 4.0],
                "suspicius_value_limits": [2, 0],
                "suspicius_maximum_limits": [1, 1],
                "suspicius_minimum_limits": [2, 0],
            },
            index=pd.date_range("2023-01-01", "2023-01-02", periods=2),
        )
        pd.testing.assert_frame_equal(result, expected)

        # Call the function under test using 'mean' as operation
        operation = "mean"
        result = generate_daily_report(data, suspicius, operation)

        # Assert the expected output
        expected = pd.DataFrame(
            {
                "value": [2.5, 5.0],
                "maximum": [5.0, 6.0],
                "minimum": [0.0, 4.0],
                "suspicius_value_limits": [2, 0],
                "suspicius_maximum_limits": [1, 1],
                "suspicius_minimum_limits": [2, 0],
            },
            index=pd.date_range("2023-01-01", "2023-01-02", periods=2),
        )
        pd.testing.assert_frame_equal(result, expected)
