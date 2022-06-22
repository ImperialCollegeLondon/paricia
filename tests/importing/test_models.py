from pathlib import Path

from django.test import TestCase


class TestSaveImportModels(TestCase):
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

    def test_save_import_temp(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        from importing.functions import preformat_matrix
        from importing.models import DataImportTemp

        matrix = preformat_matrix(self.data_file, self.file_format)
        start_date = matrix.loc[0, "date"]
        end_date = matrix.loc[matrix.shape[0] - 1, "date"]

        # Note: This sample file is not used by any functions
        sample_file = SimpleUploadedFile(
            content=b"some data file", name="test_upload.csv"
        )

        DataImportTemp.objects.create(
            station=self.station,
            format=self.file_format,
            start_date=start_date,
            end_date=end_date,
            file=sample_file,
        )

        retrieved_dit = DataImportTemp.objects.get(data_import_id=1)
        self.assertEqual(retrieved_dit.station, self.station)
        self.assertEqual(retrieved_dit.format, self.file_format)
