from datetime import datetime
from pathlib import Path
from unittest.mock import Mock, patch

import numpy as np
import pandas as pd
from django.test import TestCase, override_settings

from formatting.models import Format


@override_settings(MEDIA_ROOT=Path(__file__).parent.parent / "test_data")
class TestThingsboardFunctions(TestCase):
    """Test suits for functions to read Thingsboard data."""

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
        from formatting.models import Classification, Format
        from importing.models import DataImport, ImportOrigin, ThingsboardImportMap
        from station.models import TIMEZONES, Station
        from variable.models import Variable

        self.data_file = str(
            Path(__file__).parent.parent / "test_data/thingsboard_test.json"
        )
        self.station = Station.objects.get(station_id=8)
        self.station.timezone = TIMEZONES[0][0]
        self.origin = ImportOrigin.objects.create(origin="Thingsboard")
        self.variable = Variable.objects.get(pk=104)
        self.format = Format.objects.create(
            owner=self.variable.owner,
            thingsboard=True,
        )
        self.classification = Classification.objects.create(
            owner=self.variable.owner,
            visibility="Public",
            format=self.format,
            variable=self.variable,
        )
        self.import_map = ThingsboardImportMap.objects.create(
            tb_variable="turbidity",
            variable=self.variable,
            tb_device_name="tb-device-001",
            station=self.station,
            owner=self.station.owner,
        )
        self.data_import = DataImport.objects.create(
            owner=self.station.owner,
            station=self.station,
            format=self.format,
            rawfile=self.data_file,
            origin=self.origin,
        )

    def test_read_thingsboard_data_to_import(self):
        """Test the read_thingsboard_data_to_import function."""
        from importing.functions import read_thingsboard_data_to_import

        df = read_thingsboard_data_to_import(
            self.data_import.rawfile, self.station.timezone
        )
        self.assertEqual(len(df), 1000)
        start_date, end_date = df["date"].iloc[0], df["date"].iloc[-1]
        self.assertEqual(
            start_date,
            pd.Timestamp(1778855732730, unit="ms").tz_localize(self.station.timezone),
        )
        self.assertEqual(
            end_date,
            pd.Timestamp(1779787177749, unit="ms").tz_localize(self.station.timezone),
        )

    def test_save_temp_data_to_permanent_thingsboard(self):
        """Test the save_temp_data_to_permanent function for thingsboard data."""
        from importing.functions import save_temp_data_to_permanent
        from measurement.models import Measurement

        start_date, end_date, num_records = save_temp_data_to_permanent(
            self.data_import
        )
        self.assertEqual(num_records, 1000)
        self.assertEqual(
            start_date,
            pd.Timestamp(1778855732730, unit="ms").tz_localize(self.station.timezone),
        )
        self.assertEqual(
            end_date,
            pd.Timestamp(1779787177749, unit="ms").tz_localize(self.station.timezone),
        )

        results = Measurement.objects.filter(
            data_import=self.data_import, variable_id=self.variable.variable_id
        )
        self.assertEqual(results.count(), 1000)

    def test_parse_thingsboard_values(self):
        """Test the parse_thingsboard_values function."""
        from importing.functions import parse_thingsboard_values

        dates = pd.to_datetime(
            [
                datetime(2026, 1, 1, 9, 0, 0),
                datetime(2026, 1, 1, 9, 5, 30),
                datetime(2026, 1, 1, 9, 15, 0),
            ]
        )
        data = pd.DataFrame(
            {
                "date": dates,
                "value": ["10.0", "25.0", "37"],
            }
        )
        parsed_data = parse_thingsboard_values(data)
        self.assertIsInstance(parsed_data["value"].iloc[0], float)

        data["value"] = ["number", "10.0", "20.0"]
        with self.assertRaises(ValueError) as msg:
            parse_thingsboard_values(data)

        self.assertEqual(
            "Failed to parse value column for Thingsboard data. Check that numerical"
            " data are provided.",
            str(msg.exception),
        )

    def test_get_processed_variable_data(self):
        """Test the get_processed_variable_data_function."""
        import zoneinfo

        from formatting.models import Classification
        from importing.functions import get_processed_variable_data

        tz = zoneinfo.ZoneInfo(self.station.timezone)
        dates = pd.to_datetime(
            [
                datetime(2026, 1, 1, 9, 0, 0),
                datetime(2026, 1, 1, 9, 5, 0),
                datetime(2026, 1, 1, 9, 15, 0),
            ]
        ).tz_localize(tz)
        data = pd.DataFrame(
            {
                "date": dates,
                "value": ["10.0", "25.0", "37.0"],
            }
        )
        classification = Classification.objects.create(
            owner=self.variable.owner,
            visibility="Public",
            format=self.format,
            variable=self.variable,
            incremental=True,
            accumulate=5,
            resolution=4,
        )
        start_date = dates[0]
        end_date = dates[-1]
        processed_data = get_processed_variable_data(
            data, classification, start_date, end_date, True
        )
        self.assertEqual(processed_data["value"].tolist(), [0.0, 60.0, 0.0, 48.0])


@override_settings(MEDIA_ROOT=Path(__file__).parent.parent / "test_data")
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

        start_date, end_date, variables_data = construct_matrix(self.data_import)
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

        self.data_import.format.format_id = 1000
        with self.assertRaises(ValueError) as msg:
            construct_matrix(self.data_import)

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
            construct_matrix(self.data_import)
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

    @override_settings(MEDIA_ROOT=Path(__file__).parent.parent / "test_data")
    def test_save_temp_data_to_permanent(self):
        """Test the save_temp_data_to_permanent function."""
        from importing.functions import save_temp_data_to_permanent
        from measurement.models import Measurement

        start_date, end_date, num_records = save_temp_data_to_permanent(
            self.data_import
        )
        expected_start_date = pd.to_datetime(
            "28/06/2014 00:00:00", format=self.file_format.datetime_format
        ).tz_localize(self.station.timezone)
        expected_end_date = pd.to_datetime(
            "04/01/2017 12:40:00", format=self.file_format.datetime_format
        ).tz_localize(self.station.timezone)

        self.assertEqual(num_records, 263370)
        self.assertEqual(start_date, expected_start_date)
        self.assertEqual(end_date, expected_end_date)

        results = Measurement.objects.filter(
            data_import=self.data_import, variable_id=10
        )
        self.assertEqual(results.count(), 263370)


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

        # Delimiter is a hexcode
        file_format = Format(
            first_row=1, delimiter=Delimiter(name="comma", character="\\x2C")
        )
        result = read_file_csv(csv_file, file_format)
        expected_result = [[4, 5, 6], [7, 8, 9]]
        self.assertEqual(result.values.tolist(), expected_result)

    def test_read_file_csv_space_delimiter(self):
        """Test the read_file_csv function with a space delimiter."""
        import io

        from formatting.models import Delimiter
        from importing.functions import read_file_csv

        # Create a sample CSV file
        csv_data = "1 2 3\n4 5 6\n7 8 9\n"
        csv_file = io.StringIO(csv_data)

        # Delimiter is a white space
        file_format = Format(
            first_row=1, delimiter=Delimiter(name="space", character=" ")
        )
        result = read_file_csv(csv_file, file_format)
        expected_result = [[4, 5, 6], [7, 8, 9]]
        self.assertEqual(result.values.tolist(), expected_result)

    def test_read_file_csv_from_path(self):
        """Test the read_file_csv function when file provided."""

        from formatting.models import Delimiter
        from importing.functions import read_file_csv

        data_file = str(
            Path(__file__).parent.parent / "test_data/iMHEA_HMT_01_HI_01_raw.csv"
        )
        file_format = Format(
            first_row=1, delimiter=Delimiter(name="comma", character=","), footer_rows=2
        )
        result = read_file_csv(data_file, file_format).values.tolist()
        # Check the first and last
        self.assertEqual(result[0][0], "28/06/2014 00:00:00")
        self.assertEqual(result[-1][0], "04/01/2017 12:30:00")


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
                    np.datetime64("2022-01-01T11:00:00"),
                    pd.Timestamp("2022-01-01 12:00:00"),
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
                    pd.Timestamp("2022-01-01 12:00:00", tz="America/New_York"),
                ],
                "value": [2, 1, 3, 4],
            }
        )
        pd.testing.assert_frame_equal(processed_data, expected_data, check_dtype=False)

    def test_process_datetime_columns_error_raised(self):
        """Test process_datetime_columns raises an error with invalid datetimes."""
        import pandas as pd

        from formatting.models import Date, Delimiter, Time
        from importing.functions import process_datetime_columns

        # Prepare test data
        data = pd.DataFrame(
            {
                "date": ["not a date"],
                "value": [1],
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
        with self.assertRaises(ValueError) as msg:
            process_datetime_columns(data, file_format, timezone)

        self.assertEqual(
            str(msg.exception),
            (
                "Failed to process datetime column(s). Ensure datetimes are provided "
                "in the correct format: %Y-%m-%d %H:%M:%S."
            ),
        )


class TestStandardiseFloats(TestCase):
    """Test suite for functions to standardise floats."""

    def test_standardise_floats_remove_comma(self):
        """Test standardise floats where commas should be removed."""
        from importing.functions import standardise_floats

        # Commas removed entirely
        df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=3),
                "values": ["10.4,", "10.5,", "10.6"],
            }
        )
        mock_classification = Mock()
        mock_classification.decimal_comma = False
        expected_df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=3),
                "values": [10.4, 10.5, 10.6],
            }
        )
        result = standardise_floats(df, mock_classification)
        pd.testing.assert_frame_equal(result, expected_df)

        # Check error raised with invalid data
        df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=2),
                "values": ["10.4,", "10:6"],
            }
        )
        with self.assertRaises(ValueError) as msg:
            standardise_floats(df, mock_classification)
        self.assertStartsWith(
            str(msg.exception),
            "Failed to parse value column. Expected values formatted with periods as "
            "decimal separators.",
        )

    def test_standardise_floats_numeric(self):
        """Test standardise_floats when the values are numeric."""
        from importing.functions import standardise_floats

        # Values provided area already floats
        df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=3),
                "values": [10.4, 10.5, 10.6],
            }
        )
        mock_classification = Mock()
        mock_classification.decimal_comma = False
        expected_df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=3),
                "values": [10.4, 10.5, 10.6],
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
                "date": pd.date_range("2026-01-01", periods=3),
                "values": ["10,4.", "10,5.", "10,6"],
            }
        )
        mock_classification = Mock()
        mock_classification.decimal_comma = True
        expected_df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=3),
                "values": [10.4, 10.5, 10.6],
            }
        )
        result = standardise_floats(df, mock_classification)
        pd.testing.assert_frame_equal(result, expected_df)

        # Check error raised with invalid data
        df = pd.DataFrame(
            {
                "date": pd.date_range("2026-01-01", periods=2),
                "values": ["10,4,", "10:6"],
            }
        )
        with self.assertRaises(ValueError) as msg:
            standardise_floats(df, mock_classification)
        self.assertStartsWith(
            str(msg.exception),
            "Failed to parse value column. Expected values formatted with commas as "
            "decimal separators.",
        )
