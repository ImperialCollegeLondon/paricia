from datetime import UTC, datetime, timedelta
from unittest.mock import MagicMock, patch

from django.core.files.storage import FileSystemStorage
from django.test import TestCase

from djangomain.dash_apps import map_layer_storage


class MapLayerStorageTests(TestCase):
    @patch(
        "djangomain.dash_apps.map_layer_storage.default_storage", spec=FileSystemStorage
    )
    def test_get_map_layer_path_file_system(self, storage_mock):
        storage_mock.path.return_value = "/path/to/test.tif"
        geotiff_path = map_layer_storage.get_map_layer_path("test.tif")
        storage_mock.path.assert_called_once_with("test.tif")
        self.assertEqual(geotiff_path, "/path/to/test.tif")

    @patch("djangomain.dash_apps.map_layer_storage.default_storage")
    @patch("djangomain.dash_apps.map_layer_storage.BlobServiceClient")
    @patch("djangomain.dash_apps.map_layer_storage.generate_blob_sas")
    @patch("djangomain.dash_apps.map_layer_storage.DefaultAzureCredential")
    @patch("djangomain.dash_apps.map_layer_storage.datetime")
    @patch("djangomain.dash_apps.map_layer_storage.BlobSasPermissions")
    def test_get_map_layer_path_azure(
        self,
        permissions_mock,
        datetime_mock,
        credential_mock,
        sas_mock,
        client_mock,
        storage_mock,
    ):
        storage_mock.account_name = "account"
        storage_mock.azure_container = "container"
        credential_mock.return_value = "credential"
        now = datetime.now(UTC)
        datetime_mock.now.return_value = now
        start = now - timedelta(minutes=15)
        expiry = now + timedelta(hours=1)
        client_mock.return_value = MagicMock()
        client_mock.return_value.get_user_delegation_key.return_value = "delegation_key"
        sas_mock.return_value = "sas_token"
        permissions_mock.return_value = "permission"
        geotiff_path = map_layer_storage.get_map_layer_path("test.tif")

        client_mock.assert_called_once_with(
            account_url="https://account.blob.core.windows.net",
            credential="credential",
        )

        client_mock.return_value.get_user_delegation_key.assert_called_once_with(
            key_start_time=start,
            key_expiry_time=expiry,
        )

        sas_mock.assert_called_once_with(
            account_name="account",
            container_name="container",
            blob_name="test.tif",
            user_delegation_key="delegation_key",
            permission="permission",
            expiry=expiry,
        )

        self.assertEqual(
            geotiff_path,
            "https://account.blob.core.windows.net/container/test.tif?sas_token",
        )

    @patch(
        "djangomain.dash_apps.map_layer_storage.default_storage", spec=FileSystemStorage
    )
    @patch("djangomain.dash_apps.map_layer_storage.xr.open_dataset")
    def test_open_netcdf(self, open_dataset_mock, storage_mock):
        storage_mock.path.return_value = "/path/to/test.nc"
        dataset_mock = MagicMock(name="dataset")
        open_dataset_mock.return_value.__enter__.return_value = dataset_mock

        with map_layer_storage.open_netcdf("test.nc") as result:
            self.assertIs(result, dataset_mock)

        storage_mock.path.assert_called_once_with("test.nc")
        open_dataset_mock.assert_called_once_with(
            "/path/to/test.nc", engine="netcdf4", decode_coords="all"
        )
        open_dataset_mock.return_value.__exit__.assert_called_once()

    @patch("djangomain.dash_apps.map_layer_storage.default_storage")
    @patch("djangomain.dash_apps.map_layer_storage._generate_sas_token")
    @patch("djangomain.dash_apps.map_layer_storage.adlfs.AzureBlobFileSystem")
    @patch("djangomain.dash_apps.map_layer_storage.xr.open_dataset")
    def test_open_netcdf_azure(
        self, open_dataset_mock, filesystem_mock, sas_mock, storage_mock
    ):
        storage_mock.account_name = "account"
        storage_mock.azure_container = "container"
        sas_mock.return_value = "sas_token"
        file_obj = MagicMock(name="file")
        dataset = MagicMock(name="dataset")
        filesystem_mock.return_value.open.return_value.__enter__.return_value = file_obj
        open_dataset_mock.return_value.__enter__.return_value = dataset

        with map_layer_storage.open_netcdf("test.nc") as result:
            self.assertIs(result, dataset)

        sas_mock.assert_called_once_with("test.nc")
        filesystem_mock.assert_called_once_with(
            account_name="account", sas_token="sas_token"
        )
        filesystem_mock.return_value.open.assert_called_once_with(
            "container/test.nc", mode="rb"
        )
        open_dataset_mock.assert_called_once_with(
            file_obj, engine="netcdf4", decode_coords="all"
        )
        open_dataset_mock.return_value.__exit__.assert_called_once()
        filesystem_mock.return_value.open.return_value.__exit__.assert_called_once()
