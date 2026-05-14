from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np
import pandas as pd
from django.test import TestCase

from formatting.models import Format


class TestMatrixFunctions(TestCase):
    """Test suite for functions to construct the matrix."""

    fixtures = [
        "management_user",
        "variable_unit",
        "variable_variable",
        "formatting_delimiter",
        "formatting_extension",
        "formatting_date",
        "formatting_time",
        "formatting_format",
        "formatting_classification",
        "station_country",
        "station_region",
        "station_ecosystem",
        "station_institution",
        "station_type",
        "station_place",
        "station_basin",
        "station_placebasin",
        "station_station",
    ]

    def setUp(self):
        """Set up the test data."""
        from importing.models import DataImport
        from station.models import TIMEZONES, Station

        self.file_format = Format.objects.get(format_id=45)
        self.data_file = str(
            Path(__file__).parent.parent / "test_data/iMHEA_HMT_01_HI_01_raw.csv"
        )
        self.station = Station.objects.get(station_id=8)
        self.station.timezone = TIMEZONES[0][0]
        self.data_import = DataImport.objects.create(
            owner=self.station.owner,
            station=self.station,
            format=self.file_format,
            rawfile=self.data_file,
        )

    def test_read_data_to_import(self):
        """Test the imported data is in the correct dimensions."""
        from importing.functions import read_data_to_import

        df = read_data_to_import(
            self.data_file, self.file_format, self.station.timezone
        )
        self.assertEqual(df.shape, (263371, 4))

    def test_validate_values(self):
        """Test the validate_values function."""
        from importing.functions import validate_values

        mock_classification = Mock()
        mock_classification.value = 1
        mock_classification.value_validator_column = 2
        mock_classification.value_validator_text = "valid"
        mock_classification.maximum = None
        mock_classification.minimum = None

        matrix = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=3),
                1: [10, 20, 30],
                2: ["valid", "invalid", "valid"],
            }
        )

        expected_data = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=3),
                "value": [10, np.nan, 30],
            }
        )
        expected_columns = [("date", "date"), (1, "value")]

        data, columns = validate_values(matrix, mock_classification)
        pd.testing.assert_frame_equal(data, expected_data)
        self.assertEqual(columns, expected_columns)

    def test_remove_nan_rows(self):
        """Test the remove_nan_rows function."""
        from importing.functions import remove_nan_rows

        data = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=4),
                "value": [10.0, np.nan, 30.0, np.nan],
                "maximum": [15.0, 25.0, 35.0, np.nan],
            }
        )
        columns = [("date", "date"), (1, "value"), (2, "maximum")]

        mock_classification = Mock()
        mock_classification.variable.name = "Variable"
        mock_classification.value = 1

        expected_data = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=3),
                "value": [10.0, np.nan, 30.0],
                "maximum": [15.0, 25.0, 35.0],
            }
        )
        cleaned_data = remove_nan_rows(data, mock_classification, columns)
        pd.testing.assert_frame_equal(cleaned_data, expected_data)

        # Check null data raises error
        data = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=4),
                "value": [np.nan] * 4,
                "maximum": [np.nan] * 4,
            }
        )

        with self.assertRaises(ValueError):
            remove_nan_rows(data, mock_classification, columns)

    def test_process_incremental_data(self):
        """Test the process_incremental_data function."""
        from importing.functions import process_incremental_data

        data = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=5),
                "value": [10.0, 25.0, 37.0, 49.0, 44.0],
            }
        )
        expected_data = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-02", periods=3),
                "value": [15.0, 12.0, 12.0],
            }
        )

        processed_data = process_incremental_data(data).reset_index(drop=True)
        pd.testing.assert_frame_equal(expected_data, processed_data)

    def test_process_cumulative_data(self):
        """Test the process_cumulative_data function."""
        from importing.functions import process_cumulative_data

        dates = pd.to_datetime(
            [
                datetime(2026, 1, 1, 9, 0, 0),
                datetime(2026, 1, 1, 9, 5, 30),
                datetime(2026, 1, 1, 9, 15, 0),
                datetime(2026, 1, 1, 9, 17, 20),
                datetime(2026, 1, 1, 9, 22, 47),
            ]
        )
        data = pd.DataFrame(
            {
                "date": dates,
                "value": [10.0, 25.0, 37.0, 40.0, 52.0],
            }
        )

        expected_dates = pd.to_datetime(
            [
                datetime(2026, 1, 1, 9, 5, 0),
                datetime(2026, 1, 1, 9, 10, 0),
                datetime(2026, 1, 1, 9, 15, 0),
                datetime(2026, 1, 1, 9, 20, 0),
                datetime(2026, 1, 1, 9, 25, 0),
            ]
        )
        expected_values = [i * 0.5 for i in [10.0, 25.0, 0.0, 77.0, 52.0]]
        expected_data = pd.DataFrame(
            {
                "date": expected_dates,
                "value": expected_values,
            }
        )
        mock_classification = Mock()
        mock_classification.resolution = 0.5
        processed_data = process_cumulative_data(
            data, mock_classification, acc=5, start_date=dates[0], end_date=dates[-1]
        ).reset_index(drop=True)
        pd.testing.assert_frame_equal(expected_data, processed_data, check_dtype=False)

    @patch("importing.functions.validate_values")
    @patch("importing.functions.standardise_floats")
    @patch("importing.functions.remove_nan_rows")
    @patch("importing.functions.process_incremental_data")
    @patch("importing.functions.process_cumulative_data")
    def test_get_processed_variable_data(
        self, cum_mock, incr_mock, nan_mock, floats_mock, validate_mock
    ):
        """Test the get_processed_variable_data function."""
        from importing.functions import get_processed_variable_data

        dates = pd.to_datetime(
            [
                datetime(2026, 1, 1, 9, 0, 0),
                datetime(2026, 1, 1, 9, 5, 30),
                datetime(2026, 1, 1, 9, 15, 0),
                datetime(2026, 1, 1, 9, 17, 20),
                datetime(2026, 1, 1, 9, 22, 47),
            ]
        )
        matrix = pd.DataFrame(
            {
                "date": dates,
                "value": [10.0, 25.0, 37.0, 40.0, 52.0],
            }
        )
        nan_mock.return_value = matrix
        floats_mock.return_value = matrix
        columns = [("date", "date"), ("value", "value")]
        validate_mock.return_value = (matrix, columns)
        incr_mock.return_value = matrix
        cum_mock.return_value = matrix

        # With cumulative data
        classification_mock = Mock()
        classification_mock.incremental = True
        classification_mock.accumulate = 3
        classification_mock.resolution = 2
        start_mock, end_mock = Mock(), Mock()

        expected_data = pd.DataFrame(
            {
                "date": dates,
                "value": [10.0, 25.0, 37.0, 40.0, 52.0],
            }
        )
        result = get_processed_variable_data(
            matrix, classification_mock, start_mock, end_mock
        )
        pd.testing.assert_frame_equal(expected_data, result)
        nan_mock.assert_called_once_with(matrix, classification_mock, columns)
        floats_mock.assert_called_once_with(matrix, classification_mock)
        validate_mock.assert_called_once_with(matrix, classification_mock)
        incr_mock.assert_called_once_with(matrix)
        cum_mock.assert_called_once_with(
            matrix, classification_mock, 3, start_mock, end_mock
        )

        # Without cumulative data
        classification_mock.accumulate = False
        expected_data = pd.DataFrame(
            {
                "date": dates,
                "value": [i * 2 for i in [10.0, 25.0, 37.0, 40.0, 52.0]],
            }
        )
        result = get_processed_variable_data(
            matrix, classification_mock, start_mock, end_mock
        )
        pd.testing.assert_frame_equal(expected_data, result)

    def test_construct_matrix(self):
        """Test the construct_matrix function."""
        from importing.functions import construct_matrix
        from variable.models import Variable

        start_date, end_date, variables_data = construct_matrix(
            self.data_file, self.file_format, self.station
        )
        self.assertEqual(len(variables_data), 2)
        self.assertEqual(len(variables_data[0][1]), 263370)
        self.assertEqual(len(variables_data[1][1]), 263370)
        var_ids = [var[0] for var in variables_data]
        vars = list(
            Variable.objects.filter(variable_id__in=var_ids).values_list(
                "variable_code", flat=True
            )
        )
        self.assertListEqual(vars, ["flow", "waterlevel"])

        data_dict = {var: data[1] for var, data in zip(vars, variables_data)}

        self.assertEqual(data_dict["flow"].value.min(), 0.0)
        self.assertEqual(data_dict["flow"].value.max(), 1624.4041)

        self.assertEqual(data_dict["waterlevel"].value.min(), 0.0)
        self.assertEqual(data_dict["waterlevel"].value.max(), 96.54)

        expected_start_date = pd.to_datetime(
            "28/06/2014 00:00:00", format=self.file_format.datetime_format
        ).tz_localize(self.station.timezone)
        expected_end_date = pd.to_datetime(
            "04/01/2017 12:40:00", format=self.file_format.datetime_format
        ).tz_localize(self.station.timezone)
        self.assertEqual(start_date, expected_start_date)
        self.assertEqual(end_date, expected_end_date)

    def test_construct_matrix_no_classifications(self):
        """Test construct_matrix raises an error with no classifications."""
        from importing.functions import construct_matrix

        format = self.file_format
        format.format_id = 1000
        with self.assertRaises(ValueError) as msg:
            construct_matrix(self.data_file, format, self.station)

        self.assertEqual(
            str(msg.exception),
            "No classifications found for this format. Please add some.",
        )

    @patch("importing.functions.read_data_to_import")
    def test_construct_matrix_max_cols(self, read_data_mock):
        """Test construct_matrix raises an error when there are not enough columns."""
        from importing.functions import construct_matrix

        read_data_mock.return_value = pd.DataFrame(
            {
                "date": ["2022-01-01 10:00:00", "2022-01-02 12:00:00"],
                "value": [1, 2],
            }
        )
        with self.assertRaises(ValueError) as msg:
            construct_matrix(self.data_file, self.file_format, self.station)
        self.assertStartsWith(str(msg.exception), "The number of columns in the file")

    @patch("importing.functions.construct_matrix")
    def test_save_temp_data_to_permanent_no_data(self, matrix_mock):
        """Test save_temp_data_to_permanent raises an error when no data to import."""
        from importing.functions import save_temp_data_to_permanent

        matrix_mock.return_value = "start date", "end date", []
        with self.assertRaises(ValueError) as msg:
            save_temp_data_to_permanent(self.data_import)

        self.assertEqual(
            str(msg.exception), "No data to import. Is the chosen format correct?"
        )


class TestReadFile(TestCase):
    """Test suite for functions to read the raw data files."""

    def test_read_file_excel(self):
        """Test the read_file_excel function."""
        import io

        from formatting.models import Delimiter
        from importing.functions import read_file_excel

        # Create a sample excel file
        data = pd.DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        excel_file = io.BytesIO()
        with pd.ExcelWriter(excel_file, engine="openpyxl") as writer:
            data.to_excel(writer, index=False, header=False)

        # File format skipping one row and using a comma as delimiter
        file_format = Format(
            first_row=1, delimiter=Delimiter(name="comma", character=",")
        )
        result = read_file_excel(excel_file, file_format)
        expected_result = [[4, 5, 6], [7, 8, 9]]
        self.assertEqual(result.values.tolist(), expected_result)

        # File format using the first row and using a comma as delimiter
        excel_file.seek(0)
        file_format = Format(
            first_row=0, delimiter=Delimiter(name="comma", character=",")
        )
        result = read_file_excel(excel_file, file_format)
        expected_result = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(result.values.tolist(), expected_result)

        # File format skipping the last row and using a comma as delimiter
        excel_file.seek(0)
        file_format = Format(
            first_row=0, footer_rows=1, delimiter=Delimiter(name="comma", character=",")
        )
        result = read_file_excel(excel_file, file_format)
        expected_result = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(result.values.tolist(), expected_result)

    def test_read_file_csv(self):
        """Test the read_file_csv function."""
        import io

        from formatting.models import Delimiter
        from importing.functions import read_file_csv

        # Create a sample CSV file
        csv_data = "1,2,3\n4,5,6\n7,8,9\n"
        csv_file = io.StringIO(csv_data)

        # File format skipping one row and using a comma as delimiter
        file_format = Format(
            first_row=1, delimiter=Delimiter(name="comma", character=",")
        )
        result = read_file_csv(csv_file, file_format)
        expected_result = [[4, 5, 6], [7, 8, 9]]
        self.assertEqual(result.values.tolist(), expected_result)

        # File format using the first row and using a comma as delimiter
        csv_file.seek(0)
        file_format = Format(
            first_row=0, delimiter=Delimiter(name="comma", character=",")
        )
        result = read_file_csv(csv_file, file_format)
        expected_result = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(result.values.tolist(), expected_result)

        # File format skipping the last row and using a comma as delimiter
        csv_file.seek(0)
        file_format = Format(
            first_row=0, footer_rows=1, delimiter=Delimiter(name="comma", character=",")
        )
        result = read_file_csv(csv_file, file_format)
        expected_result = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(result.values.tolist(), expected_result)


class TestProcessDatetimeColumns(TestCase):
    """Test suite for processing the datetime columns."""

    def test_process_datetime_columns_same_column(self):
        """Test process_datetime_columns when date and time are in the same column."""
        import pandas as pd

        from formatting.models import Date, Delimiter, Time
        from importing.functions import process_datetime_columns

        # Prepare test data
        data = pd.DataFrame(
            {
                "date": ["2022-01-01 10:00:00", "2022-01-02 12:00:00"],
                "value": [1, 2],
            }
        )
        file_format = Format(
            first_row=0,
            date_column=0,
            time_column=0,
            date=Date(date_format="", code="%Y-%m-%d"),
            time=Time(time_format="", code="%H:%M:%S"),
            delimiter=Delimiter(name="comma", character=","),
        )
        timezone = "America/New_York"

        # Call the function
        processed_data = process_datetime_columns(data, file_format, timezone)

        # Assert the result
        expected_data = pd.DataFrame(
            {
                "date": [
                    pd.Timestamp("2022-01-01 10:00:00", tz="America/New_York"),
                    pd.Timestamp("2022-01-02 12:00:00", tz="America/New_York"),
                ],
                "value": [1, 2],
            }
        )
        pd.testing.assert_frame_equal(
            processed_data[["date", "value"]], expected_data, check_dtype=False
        )

    def test_process_datetime_columns_different_columns(self):
        """Test process_datetime_columns when datetime in a single column."""
        import pandas as pd

        from formatting.models import Date, Delimiter, Time
        from importing.functions import process_datetime_columns

        # Prepare test data
        data = pd.DataFrame(
            {
                "date": ["2022-01-01", "2022-01-02"],
                "time": ["10:00:00", "12:00:00"],
                "value": [1, 2],
            }
        )
        file_format = Format(
            first_row=0,
            date_column=0,
            time_column=1,
            date=Date(date_format="", code="%Y-%m-%d"),
            time=Time(time_format="", code="%H:%M:%S"),
            delimiter=Delimiter(name="coma", character=","),
        )
        timezone = "America/New_York"

        # Call the function
        processed_data = process_datetime_columns(data, file_format, timezone)

        # Assert the result
        expected_data = pd.DataFrame(
            {
                "date": [
                    pd.Timestamp("2022-01-01 10:00:00", tz="America/New_York"),
                    pd.Timestamp("2022-01-02 12:00:00", tz="America/New_York"),
                ],
                "value": [1, 2],
            }
        )
        pd.testing.assert_frame_equal(
            processed_data[["date", "value"]], expected_data, check_dtype=False
        )

    def test_process_datetime_columns_different_formats(self):
        """Test process_datetime_columns when there are different date formats."""
        import pandas as pd

        from formatting.models import Date, Delimiter, Time
        from importing.functions import process_datetime_columns

        # Prepare test data
        data = pd.DataFrame(
            {
                "date": [
                    datetime(2022, 1, 1, 10, 0, 0),
                    "2022-01-01 09:00:00",
                    "not a date",
                    np.datetime64("2022-01-01T11:00:00"),
                ],
                "value": [1, 2, 3, 4],
            }
        )
        file_format = Format(
            first_row=0,
            date_column=0,
            time_column=0,
            date=Date(date_format="", code="%Y-%m-%d"),
            time=Time(time_format="", code="%H:%M:%S"),
            delimiter=Delimiter(name="comma", character=","),
        )
        timezone = "America/New_York"

        # Call the function
        processed_data = process_datetime_columns(data, file_format, timezone)

        # Assert the result
        expected_data = pd.DataFrame(
            {
                "date": [
                    pd.Timestamp("2022-01-01 09:00:00", tz="America/New_York"),
                    pd.Timestamp("2022-01-01 10:00:00", tz="America/New_York"),
                    pd.Timestamp("2022-01-01 11:00:00", tz="America/New_York"),
                    pd.NaT,
                ],
                "value": [2, 1, 4, 3],
            }
        )
        pd.testing.assert_frame_equal(processed_data, expected_data, check_dtype=False)


class TestStandardiseFloats(TestCase):
    """Test suite for functions to standardise floats."""

    def test_standardise_floats_remove_comma(self):
        """Test standardise floats where commas should be removed."""
        from importing.functions import standardise_floats

        # Commas removed entirely
        df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=4),
                "values": ["10.4,", "10.5,", "10.6", "10:7"],
            }
        )
        mock_classification = Mock()
        mock_classification.decimal_comma = False
        expected_df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=4),
                "values": [10.4, 10.5, 10.6, np.nan],
            }
        )
        result = standardise_floats(df, mock_classification)
        pd.testing.assert_frame_equal(result, expected_df)

    def test_standardise_floats_numeric(self):
        """Test standardise_floats when the values are numeric."""
        from importing.functions import standardise_floats

        # Values provided area already floats
        df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=4),
                "values": [10.4, 10.5, 10.6, np.nan],
            }
        )
        mock_classification = Mock()
        mock_classification.decimal_comma = False
        expected_df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=4),
                "values": [10.4, 10.5, 10.6, np.nan],
            }
        )
        result = standardise_floats(df, mock_classification)
        pd.testing.assert_frame_equal(result, expected_df)

    def test_standardise_floats_replace_commas(self):
        """Test standardise_floats where commas should be changed to periods."""
        from importing.functions import standardise_floats

        # Periods removed and commas replaced by periods
        df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=4),
                "values": ["10,4.", "10,5.", "10,6", "10:7"],
            }
        )
        mock_classification = Mock()
        mock_classification.decimal_comma = True
        expected_df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=4),
                "values": [10.4, 10.5, 10.6, np.nan],
            }
        )
        result = standardise_floats(df, mock_classification)
        pd.testing.assert_frame_equal(result, expected_df)
