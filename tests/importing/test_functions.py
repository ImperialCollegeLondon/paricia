from datetime import datetime
from pathlib import Path

import pytz
from django.test import TestCase


class TestMatrixFunctions(TestCase):
    fixtures = [
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
        from formatting.models import Format
        from station.models import TIMEZONES, Station

        self.file_format = Format.objects.get(format_id=45)
        self.data_file = str(
            Path(__file__).parent.parent / "test_data/iMHEA_HMT_01_HI_01_raw.csv"
        )
        self.station = Station.objects.get(station_id=8)
        self.station.timezone = TIMEZONES[0][0]

    def test_preformat_matrix(self):
        from importing.functions import read_data_to_import

        df = read_data_to_import(
            self.data_file, self.file_format, self.station.timezone
        )
        self.assertEqual(df.shape, (263371, 5))

    def test_construct_matrix(self):
        from importing.functions import construct_matrix
        from variable.models import Variable

        variables_data = construct_matrix(
            self.data_file, self.file_format, self.station
        )
        self.assertEqual(len(variables_data), 2)
        vars = list(
            Variable.objects.filter(
                variable_id__in=[var["variable_id"][0] for var in variables_data]
            ).values_list("variable_code", flat=True)
        )
        self.assertListEqual(vars, ["flow", "waterlevel"])

        data_dict = {var: data for var, data in zip(vars, variables_data)}

        self.assertEqual(data_dict["flow"].value.min(), 0.0)
        self.assertEqual(data_dict["flow"].value.max(), 1624.4041)

        self.assertEqual(data_dict["waterlevel"].value.min(), 0.0)
        self.assertEqual(data_dict["waterlevel"].value.max(), 96.54)


class TestDateFunctions(TestCase):
    fixtures = [
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
        from django.core.files.uploadedfile import SimpleUploadedFile

        from formatting.models import Format
        from importing.functions import read_data_to_import
        from importing.models import DataImport
        from measurement.models import Measurement
        from station.models import TIMEZONES, Station
        from variable.models import Variable

        self.file_format = Format.objects.get(format_id=45)
        self.data_file = str(
            Path(__file__).parent.parent / "test_data" / "iMHEA_HMT_01_HI_01_raw.csv"
        )
        self.station = Station.objects.get(station_id=8)
        self.variable = Variable.objects.get(variable_id=10)
        self.station.timezone = TIMEZONES[0][0]

        matrix = read_data_to_import(
            self.data_file, self.file_format, self.station.timezone
        )
        start_date = matrix.loc[0, "date"]
        end_date = matrix.loc[matrix.shape[0] - 1, "date"]

        # Note: This sample file is not used by any functions
        sample_file = SimpleUploadedFile(
            content=b"some data file", name="test_upload.csv"
        )

        self.data_import = DataImport.objects.create(
            station=self.station,
            format=self.file_format,
            start_date=start_date,
            end_date=end_date,
            rawfile=sample_file,
            records=matrix.shape[0],
        )

        # Two lines of dummy data from the actual file
        Measurement.objects.create(
            station=self.station,
            variable=self.variable,
            time=datetime(2014, 6, 28, 0, 35, 0, tzinfo=pytz.UTC),
            value=3.4,
        )
        Measurement.objects.create(
            station=self.station,
            variable=self.variable,
            time=datetime(2016, 3, 7, 18, 5, 0, tzinfo=pytz.UTC),
            value=5.7,
        )

    def test_get_last_uploaded_date(self):
        from importing.functions import get_last_uploaded_date

        self.assertEqual(get_last_uploaded_date(8, "flow").year, 2016)

    def test_validate_dates(self):
        from importing.functions import validate_dates

        validation = validate_dates(self.data_import)
        self.assertEqual(validation[0][0]["variable_code"], "flow")
        self.assertTrue(validation[0][0]["exists"])
        self.assertEqual(validation[0][1]["variable_code"], "waterlevel")
        self.assertFalse(validation[0][1]["exists"])
        self.assertEqual(validation[1], True)


class TestReadFileCSV(TestCase):
    def test_read_file_csv(self):
        import io

        from formatting.models import Delimiter, Format
        from importing.functions import read_file_csv

        # Create a sample CSV file
        csv_data = "1,2,3\n4,5,6\n7,8,9\n"
        csv_file = io.StringIO(csv_data)

        # File format skipping one row
        # and using a coma as delimiter
        file_format = Format(
            first_row=1, delimiter=Delimiter(name="coma", character=",")
        )
        result = read_file_csv(csv_file, file_format)
        expected_result = [[4, 5, 6], [7, 8, 9]]
        self.assertEqual(result.values.tolist(), expected_result)

        # File format using the first row and a coma as delimiter
        csv_file.seek(0)
        file_format = Format(
            first_row=0, delimiter=Delimiter(name="coma", character=",")
        )
        result = read_file_csv(csv_file, file_format)
        expected_result = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        self.assertEqual(result.values.tolist(), expected_result)

        # File format skipping the last row and using a coma as delimiter
        csv_file.seek(0)
        file_format = Format(
            first_row=0, footer_rows=1, delimiter=Delimiter(name="coma", character=",")
        )
        result = read_file_csv(csv_file, file_format)
        expected_result = [[1, 2, 3], [4, 5, 6]]
        self.assertEqual(result.values.tolist(), expected_result)


class TestProcessDatetimeColumns(TestCase):
    def test_process_datetime_columns_same_column(self):
        import pandas as pd

        from formatting.models import Date, Delimiter, Format, Time
        from importing.functions import process_datetime_columns

        # Prepare test data
        data = pd.DataFrame(
            {
                "datetime": ["2022-01-01 10:00:00", "2022-01-02 12:00:00"],
                "value": [1, 2],
            }
        )
        file_format = Format(
            first_row=0,
            date_column=0,
            time_column=0,
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

    def test_process_datetime_columns_different_columns(self):
        import pandas as pd

        from formatting.models import Date, Delimiter, Format, Time
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
