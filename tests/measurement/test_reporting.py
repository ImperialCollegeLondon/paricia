import zoneinfo
from datetime import datetime
from decimal import Decimal
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from django.test import TestCase
from model_bakery import baker


class TestReporting(TestCase):
    def setUp(self):
        from station.models import Station
        from variable.models import Variable

        self.station = baker.make(Station)
        self.variable = baker.make(Variable)

    def test_calculate_reports(self):
        from measurement.reporting import calculate_reports

        # Create sample data
        time = pd.date_range(
            start="2023-01-01", end="2023-01-03", freq="5min", inclusive="left"
        )
        data = pd.DataFrame(
            {
                "time": time,
                "value": np.linspace(1, 5, len(time)),
                "maximum": np.linspace(1, 5, len(time)) + 1,
                "minimum": np.linspace(1, 5, len(time)) - 1,
            }
        )

        # Define test parameters
        station = "Station A"
        variable = "Variable X"
        operation = "mean"
        period = Decimal(5)

        # Call the function under test
        result = calculate_reports(data, station, variable, operation, period)

        # Assert some content
        self.assertListEqual(
            list(result["report_type"].unique()), ["hourly", "daily", "monthly"]
        )
        self.assertListEqual(list(result["station"].unique()), [station])
        self.assertListEqual(list(result["variable"].unique()), [variable])

        # Assert general shape and size
        self.assertEqual(len(result[result["report_type"] == "hourly"]), 48)
        self.assertEqual(len(result[result["report_type"] == "daily"]), 2)
        self.assertEqual(len(result[result["report_type"] == "monthly"]), 1)
        self.assertListEqual(
            list(result.columns),
            [
                "value",
                "maximum",
                "minimum",
                "completeness",
                "report_type",
                "station",
                "variable",
            ],
        )

        # Assert the time column is rounded to the nearest hour
        times = result.index.to_series()
        pd.testing.assert_series_equal(times, times.dt.round("H"))

    def test_reformat_dates(self):
        from measurement.reporting import reformat_dates

        # Define test parameters
        station = self.station.station_code
        start_time = "2023-01-01"
        end_time = "2023-12-31"

        # Call the function under test
        result = reformat_dates(station, start_time, end_time)

        # Assert the start and end dates
        expected_start_time = datetime(
            2023, 1, 1, tzinfo=ZoneInfo(self.station.timezone)
        )
        expected_end_time = datetime(
            2023, 12, 31, 23, 59, 59, tzinfo=ZoneInfo(self.station.timezone)
        )
        self.assertEqual(result[0], expected_start_time)
        self.assertEqual(result[1], expected_end_time)

    def test_get_data_to_report(self):
        from measurement.models import Measurement
        from measurement.reporting import get_data_to_report

        # Create sample data
        tz = zoneinfo.ZoneInfo(self.station.timezone)
        start_time = datetime(2023, 1, 1, 0, 0, tzinfo=tz)
        end_time = datetime(2023, 1, 3, 0, 0, tzinfo=tz)

        # Create mock Measurement objects
        measurements = [
            Measurement(
                station=self.station,
                variable=self.variable,
                time=start_time,
                value=1.0,
                is_active=True,
            ),
            Measurement(
                station=self.station,
                variable=self.variable,
                time=end_time,
                value=5.0,
                is_active=True,
            ),
        ]
        Measurement.objects.bulk_create(measurements)

        # Call the function under test
        result = get_data_to_report(
            self.station.station_code, self.variable.variable_code, start_time, end_time
        )

        # Assert the result
        self.assertEqual(len(result), 2)
        self.assertIn("value", result.columns)
        self.assertIn("time", result.columns)
        self.assertEqual(result["station_id"].unique()[0], self.station.station_id)
        self.assertEqual(result["variable_id"].unique()[0], self.variable.variable_id)
        self.assertEqual(result["time"].min(), start_time)
        self.assertEqual(result["time"].max(), end_time)

    def test_remove_report_data_in_range(self):
        from measurement.models import Report
        from measurement.reporting import remove_report_data_in_range

        # Create sample data
        tz = zoneinfo.ZoneInfo(self.station.timezone)
        start_time = datetime(2023, 1, 1, 0, 0, tzinfo=tz)
        end_time = datetime(2023, 1, 3, 0, 0, tzinfo=tz)

        # Create mock Report objects
        reports = [
            Report(
                station=self.station,
                variable=self.variable,
                time=start_time,
                value=1.0,
                completeness=1.0,
                report_type="hourly",
            ),
            Report(
                station=self.station,
                variable=self.variable,
                time=end_time,
                value=5.0,
                completeness=1.0,
                report_type="hourly",
            ),
        ]
        Report.objects.bulk_create(reports)

        # Call the function under test
        remove_report_data_in_range(
            self.station.station_code, self.variable.variable_code, start_time, end_time
        )

        # Assert the data is removed from the database
        self.assertEqual(
            Report.objects.filter(
                station__station_code=self.station.station_code
            ).count(),
            0,
        )

    def test_save_report_data(self):
        from measurement.models import Report
        from measurement.reporting import save_report_data

        # Create sample data
        time = (
            pd.Timestamp("2023-01-01")
            .replace(tzinfo=ZoneInfo(self.station.timezone))
            .to_pydatetime()
        )
        data = pd.DataFrame(
            {
                "station": [self.station.station_code],
                "variable": [self.variable.variable_code],
                "time": time,
                "value": [1.0],
                "completeness": [1.0],
                "report_type": ["hourly"],
            }
        ).set_index("time")

        # Call the function under test
        save_report_data(data)

        # Assert the data is saved in the database
        report = Report.objects.get(
            station=self.station,
            variable=self.variable,
            time=time,
            value=1.0,
            completeness=1.0,
            report_type="hourly",
        )
        self.assertEqual(report.station, self.station)
        self.assertEqual(report.variable, self.variable)
        self.assertEqual(report.time, time)
        self.assertEqual(report.value, 1.0)
        self.assertEqual(report.completeness, 1.0)
        self.assertEqual(report.report_type, "hourly")

    def test_get_report_data(self):
        from measurement.models import Report
        from measurement.reporting import get_report_data_from_db

        # Create sample data
        start_time = "2023-01-01"
        end_time = "2023-01-03"
        report_type = "hourly"

        # Create mock Report objects
        time1 = (
            pd.Timestamp("2023-01-01")
            .replace(tzinfo=ZoneInfo(self.station.timezone))
            .to_pydatetime()
        )
        time2 = (
            pd.Timestamp("2023-01-02")
            .replace(tzinfo=ZoneInfo(self.station.timezone))
            .to_pydatetime()
        )
        reports = [
            Report(
                station=self.station,
                variable=self.variable,
                time=time1,
                value=1.0,
                completeness=1.0,
                report_type=report_type,
            ),
            Report(
                station=self.station,
                variable=self.variable,
                time=time2,
                value=2.0,
                completeness=1.0,
                report_type=report_type,
            ),
        ]
        Report.objects.bulk_create(reports)

        # Call the function under test
        result = get_report_data_from_db(
            self.station.station_code,
            self.variable.variable_code,
            start_time,
            end_time,
            report_type,
        )

        # Assert the result
        self.assertIsInstance(result, pd.DataFrame)
        self.assertEqual(len(result), 2)
        self.assertListEqual(
            list(result.columns),
            [
                "id",
                "time",
                "station",
                "variable",
                "value",
                "maximum",
                "minimum",
                "report_type",
                "completeness",
            ],
        )
        self.assertEqual(result["station"].unique()[0], self.station.station_id)
        self.assertEqual(result["variable"].unique()[0], self.variable.variable_id)
        self.assertEqual(result["time"].min(), time1)
        self.assertEqual(result["time"].max(), time2)
