from decimal import Decimal

import numpy as np
import pandas as pd
from django.test import TestCase


class TestReporting(TestCase):
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
