from datetime import datetime, timedelta

import pandas as pd
from django.test import TestCase

from measurement.dash_apps.plots import add_nans_for_gaps


class TestAddNansForGaps(TestCase):
    """Tests for the add_nans_for_gaps function."""

    def test_no_gaps(self):
        """Test that data with no gaps is returned unchanged (except sorted)."""
        data = pd.DataFrame(
            {
                "time": [
                    datetime(2023, 1, 1, 10, 0),
                    datetime(2023, 1, 1, 10, 10),
                    datetime(2023, 1, 1, 10, 20),
                ],
                "value": [1.0, 2.0, 3.0],
                "maximum": [1.5, 2.5, 3.5],
                "minimum": [0.5, 1.5, 2.5],
            }
        )
        result = add_nans_for_gaps(data)
        # Should be sorted and have no NaNs added
        assert len(result) == 3
        assert result["value"].isna().sum() == 0
        pd.testing.assert_frame_equal(
            result[["time", "value", "maximum", "minimum"]],
            data.sort_values("time").reset_index(drop=True),
        )

    def test_single_gap(self):
        """Test adding NaN for a single gap."""
        base_time = datetime(2023, 1, 1, 10, 0)
        data = pd.DataFrame(
            {
                "time": [
                    base_time,
                    base_time + timedelta(minutes=10),
                    base_time
                    + timedelta(minutes=50),  # Gap here (40 min > 15 min threshold)
                ],
                "value": [1.0, 2.0, 3.0],
                "maximum": [1.5, 2.5, 3.5],
                "minimum": [0.5, 1.5, 2.5],
            }
        )
        result = add_nans_for_gaps(data)
        # Should have 4 rows: 3 original + 1 NaN
        assert len(result) == 4
        # One NaN value
        assert result["value"].isna().sum() == 1
        # The NaN row should have maximum and minimum from the row after the gap
        nan_row = result[result["value"].isna()].iloc[0]
        assert nan_row["maximum"] == 3.5
        assert nan_row["minimum"] == 2.5

    def test_multiple_gaps(self):
        """Test adding NaNs for multiple gaps."""
        base_time = datetime(2023, 1, 1, 10, 0)
        data = pd.DataFrame(
            {
                "time": [
                    base_time,
                    base_time + timedelta(minutes=10),
                    base_time + timedelta(minutes=50),  # Gap 1
                    base_time + timedelta(minutes=60),
                    base_time + timedelta(minutes=120),  # Gap 2
                ],
                "value": [1.0, 2.0, 3.0, 4.0, 5.0],
                "maximum": [1.5, 2.5, 3.5, 4.5, 5.5],
                "minimum": [0.5, 1.5, 2.5, 3.5, 4.5],
            }
        )
        result = add_nans_for_gaps(data)
        # Should have 7 rows: 5 original + 2 NaN
        assert len(result) == 7
        assert result["value"].isna().sum() == 2

    def test_empty_dataframe(self):
        """Test with empty DataFrame."""
        data = pd.DataFrame(columns=["time", "value", "maximum", "minimum"])
        result = add_nans_for_gaps(data)
        assert len(result) == 0

    def test_single_row(self):
        """Test with single row - no gaps possible."""
        data = pd.DataFrame(
            {
                "time": [datetime(2023, 1, 1, 10, 0)],
                "value": [1.0],
                "maximum": [1.5],
                "minimum": [0.5],
            }
        )
        result = add_nans_for_gaps(data)
        pd.testing.assert_frame_equal(result, data)

    def test_unsorted_data(self):
        """Test that unsorted data gets sorted."""
        data = pd.DataFrame(
            {
                "time": [
                    datetime(2023, 1, 1, 10, 20),
                    datetime(2023, 1, 1, 10, 0),
                    datetime(2023, 1, 1, 10, 10),
                ],
                "value": [3.0, 1.0, 2.0],
                "maximum": [3.5, 1.5, 2.5],
                "minimum": [2.5, 0.5, 1.5],
            }
        )
        result = add_nans_for_gaps(data)
        # Should be sorted by time
        assert result["time"].is_monotonic_increasing
        assert list(result["value"]) == [1.0, 2.0, 3.0]
