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
        from importing.models import DataImportTemp
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

        self.data_import_temp = DataImportTemp.objects.create(
            station=self.station,
            format=self.file_format,
            start_date=start_date,
            end_date=end_date,
            file=sample_file,
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

        validation = validate_dates(self.data_import_temp)
        self.assertEqual(validation[0][0]["variable_code"], "flow")
        self.assertTrue(validation[0][0]["exists"])
        self.assertEqual(validation[0][1]["variable_code"], "waterlevel")
        self.assertFalse(validation[0][1]["exists"])
        self.assertEqual(validation[1], True)
