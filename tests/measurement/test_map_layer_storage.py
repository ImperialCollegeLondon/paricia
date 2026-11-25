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
