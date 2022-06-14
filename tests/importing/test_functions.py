from pathlib import Path

from django.test import TestCase


class TestUploadData(TestCase):
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
        from station.models import Station

        self.file_format = Format.objects.get(format_id=45)
        self.data_file = str(
            Path(__file__).parent.parent / "test_data/iMHEA_HMT_01_HI_01_raw.csv"
        )
        self.station = Station.objects.get(station_id=8)

    def test_preformat_matrix(self):
        from importing.functions import preformat_matrix

        df = preformat_matrix(self.data_file, self.file_format)
        self.assertEqual(df.shape, (263371, 5))

    def test_construct_matrix(self):
        from importing.functions import construct_matrix

        variables_data = construct_matrix(
            self.data_file, self.file_format, self.station
        )
        self.assertEqual(list(variables_data.keys()), [10, 11])

        self.assertEqual(variables_data[10].value.min(), 0.0)
        self.assertEqual(variables_data[10].value.max(), 1624.4041)

        self.assertEqual(variables_data[11].value.min(), 0.0)
        self.assertEqual(variables_data[11].value.max(), 96.54)
