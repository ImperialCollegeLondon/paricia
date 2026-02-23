from pathlib import Path

from django.core.exceptions import ValidationError
from django.test import TestCase


class TestSaveImportModels(TestCase):
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
        from formatting.models import Format
        from station.models import TIMEZONES, Station

        self.file_format = Format.objects.get(format_id=45)
        self.data_file = str(
            Path(__file__).parent.parent / "test_data/iMHEA_HMT_01_HI_01_raw.csv"
        )
        self.station = Station.objects.get(station_id=8)
        self.station.timezone = TIMEZONES[0][0]

    def test_save_import(self):
        from django.core.files.uploadedfile import SimpleUploadedFile

        from importing.functions import read_data_to_import
        from importing.models import DataImport

        matrix = read_data_to_import(
            self.data_file, self.file_format, self.station.timezone
        )
        start_date = matrix.loc[0, "date"]
        end_date = matrix.loc[matrix.shape[0] - 1, "date"]

        # Note: This sample file is not used by any functions
        sample_file = SimpleUploadedFile(
            content=b"some data file", name="test_upload.csv"
        )

        DataImport.objects.create(
            owner=self.station.owner,
            station=self.station,
            format=self.file_format,
            start_date=start_date,
            end_date=end_date,
            rawfile=sample_file,
            records=matrix.shape[0],
        )

        retrieved_dit = DataImport.objects.get_queryset()[0]
        self.assertEqual(retrieved_dit.station, self.station)
        self.assertEqual(retrieved_dit.format, self.file_format)


class TestThingsboardImportMap(TestCase):
    fixtures = [
        "management_user",
        "variable_unit",
        "variable_variable",
        "sensor_type",
        "sensor_brand",
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
        from sensor.models import Sensor, SensorBrand, SensorType
        from station.models import Station
        from variable.models import SensorInstallation, Variable

        self.station = Station.objects.get(station_id=8)
        self.variable = Variable.objects.get(variable_id=1)
        self.other_variable = Variable.objects.get(variable_id=2)

        sensor_type = SensorType.objects.get(type_id=1)
        sensor_brand = SensorBrand.objects.get(brand_id=1)
        self.sensor = Sensor.objects.create(
            code="TEST_SENSOR_01",
            sensor_type=sensor_type,
            sensor_brand=sensor_brand,
            owner=self.station.owner,
        )

        self.sensor_installation = SensorInstallation.objects.create(
            variable=self.variable,
            station=self.station,
            sensor=self.sensor,
            start_date="2020-01-01",
            owner=self.station.owner,
        )

    def test_create_thingsboard_import_map(self):
        from importing.models import ThingsboardImportMap

        mapping = ThingsboardImportMap.objects.create(
            tb_variable="Test Variable",
            variable=self.variable,
            device_id="tb-device-001",
            station=self.station,
        )

        retrieved = ThingsboardImportMap.objects.get(pk=mapping.pk)
        self.assertEqual(retrieved.tb_variable, "Test Variable")
        self.assertEqual(retrieved.variable, self.variable)
        self.assertEqual(retrieved.device_id, "tb-device-001")
        self.assertEqual(retrieved.station, self.station)

    def test_str(self):
        from importing.models import ThingsboardImportMap

        mapping = ThingsboardImportMap(
            tb_variable="Test Variable",
            variable=self.variable,
            device_id="tb-device-001",
            station=self.station,
        )

        self.assertEqual(
            str(mapping),
            f"tb-device-001 -> {self.station}: Test Variable -> {self.variable}",
        )

    def test_clean_valid_variable(self):
        from importing.models import ThingsboardImportMap

        mapping = ThingsboardImportMap(
            tb_variable="Valid Variable",
            variable=self.variable,
            device_id="tb-device-002",
            station=self.station,
        )
        # Should not raise any errors
        mapping.clean()

    def test_clean_invalid_variable(self):
        from importing.models import ThingsboardImportMap

        mapping = ThingsboardImportMap(
            tb_variable="Invalid Variable",
            variable=self.other_variable,
            device_id="tb-device-003",
            station=self.station,
        )
        with self.assertRaises(ValidationError) as ctx:
            mapping.clean()

        self.assertIn("variable", ctx.exception.message_dict)


class TestImportOrigin(TestCase):
    def test_get_default(self):
        from importing.models import ImportOrigin

        result = ImportOrigin.get_default()
        assert ImportOrigin.objects.get(pk=result).origin == "file"