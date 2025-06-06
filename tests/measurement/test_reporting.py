from datetime import datetime
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
                "data_import_id": None,
                "value": np.linspace(1, 5, len(time)),
                "maximum": np.linspace(1, 5, len(time)) + 1,
                "minimum": np.linspace(1, 5, len(time)) - 1,
            }
        )

        # Define test parameters
        station = "Station A"
        variable = "Variable X"
        operation = "mean"
        # Call the function under test
        result = calculate_reports(data, station, variable, operation)

        # Assert some content
        self.assertListEqual(
            list(result["report_type"].unique()), ["hourly", "daily", "monthly"]
        )
        self.assertListEqual(list(result["station"].unique()), [station])
        self.assertListEqual(list(result["variable"].unique()), [variable])

        # Assert general shape and size
        self.assertListEqual(
            list(result.columns),
            [
                "value",
                "maximum",
                "minimum",
                "data_import_id",
                "report_type",
                "station",
                "variable",
            ],
        )

        # Assert the time column is rounded to the nearest hour
        times = result.index.to_series()
        pd.testing.assert_series_equal(times, times.dt.round("h"))

    def test_reformat_dates(self):
        from django.utils import timezone

        from measurement.reporting import reformat_dates

        # Define test parameters
        tz = timezone.get_current_timezone()
        start_time = "2023-01-06"
        end_time = "2023-12-15"

        # Call the function under test
        result = reformat_dates(start_time, end_time)

        # Assert the start and end dates
        expected_start_time = datetime(2023, 1, 1, tzinfo=tz)
        expected_end_time = datetime(2023, 12, 31, 23, 59, 59, tzinfo=tz)
        self.assertEqual(result[0], expected_start_time)
        self.assertEqual(result[1], expected_end_time)

    def test_reformat_dates_partial_months(self):
        from django.utils import timezone

        from measurement.reporting import reformat_dates

        # Define test parameters
        tz = timezone.get_current_timezone()
        start_time = "2023-01-06"
        end_time = "2023-12-15"

        # Call the function under test
        result = reformat_dates(start_time, end_time, whole_months=False)

        # Assert the start and end dates
        expected_start_time = datetime(2023, 1, 6, tzinfo=tz)
        expected_end_time = datetime(2023, 12, 15, 23, 59, 59, tzinfo=tz)
        self.assertEqual(result[0], expected_start_time)
        self.assertEqual(result[1], expected_end_time)

    def test_get_data_to_report(self):
        from django.utils import timezone

        from measurement.models import Measurement
        from measurement.reporting import get_data_to_report

        # Create sample data
        tz = timezone.get_current_timezone()
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
        from django.utils import timezone

        from measurement.models import Report
        from measurement.reporting import remove_report_data_in_range

        # Create sample data
        tz = timezone.get_current_timezone()
        start_time = datetime(2023, 1, 1, 0, 0, tzinfo=tz)
        end_time = datetime(2023, 1, 3, 0, 0, tzinfo=tz)

        # Create mock Report objects
        reports = [
            Report(
                station=self.station,
                variable=self.variable,
                time=start_time,
                value=1.0,
                report_type="hourly",
            ),
            Report(
                station=self.station,
                variable=self.variable,
                time=end_time,
                value=5.0,
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
                "data_import_id": [None],
                "time": time,
                "value": [1.0],
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
            report_type="hourly",
        )
        self.assertEqual(report.station, self.station)
        self.assertEqual(report.variable, self.variable)
        self.assertEqual(report.time, time)
        self.assertEqual(report.value, 1.0)
        self.assertEqual(report.report_type, "hourly")

    def test_get_report_data(self):
        from django.utils import timezone

        from measurement.models import Report
        from measurement.reporting import get_report_data_from_db

        # Create sample data
        start_time = "2023-01-01"
        end_time = "2023-01-03"
        report_type = "hourly"
        tz = timezone.get_current_timezone()

        # Create mock Report objects
        time1 = pd.Timestamp("2023-01-01").replace(tzinfo=tz).to_pydatetime()
        time2 = pd.Timestamp("2023-01-02").replace(tzinfo=tz).to_pydatetime()
        reports = [
            Report(
                station=self.station,
                variable=self.variable,
                time=time1,
                value=1.0,
                report_type=report_type,
            ),
            Report(
                station=self.station,
                variable=self.variable,
                time=time2,
                value=2.0,
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
                "data_import_id",
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

    def test_launch_reports_calculation(self):
        from measurement.models import Measurement
        from measurement.reporting import (
            get_report_data_from_db,
            launch_reports_calculation,
            reformat_dates,
        )

        self.station.clean()
        self.station.save()

        # Define test parameters
        station = self.station.station_code
        variable = self.variable.variable_code
        start_time = "2023-01-01"
        end_time = "2023-01-03"

        self.variable.nature = "value"
        self.variable.save()

        start_time_, end_time_ = reformat_dates(start_time, end_time)

        # Create mock Measurement objects
        measurements = [
            Measurement(
                station=self.station,
                variable=self.variable,
                time=start_time_,
                value=1.0,
                is_active=True,
            ),
            Measurement(
                station=self.station,
                variable=self.variable,
                time=end_time_,
                value=5.0,
                is_active=True,
            ),
        ]
        Measurement.objects.bulk_create(measurements)

        # Assert no report data is present in the database
        for report_type in ["hourly", "daily", "monthly"]:
            report = get_report_data_from_db(
                station, variable, start_time, end_time, report_type
            )
            self.assertEqual(len(report), 0)

        get_report_data_from_db.cache_clear()

        # Call the function under test. If the function is working correctly, it will
        # serves as integration tests for all the functions used in the process.
        launch_reports_calculation(station, variable, start_time, end_time)

        # Assert report data is present in the database
        for report_type in ["hourly", "daily", "monthly"]:
            report = get_report_data_from_db(
                station, variable, start_time, end_time, report_type
            )
            self.assertGreaterEqual(len(report), 1)
