from unittest.mock import MagicMock, patch

from django.test import TestCase

from importing.utils import retrieve_thingsboard_data, retrieve_thingsboard_device_id


class RetrieveThingsboardDeviceIdTest(TestCase):
    """Tests for retrieve_thingsboard_device_id."""

    @patch("importing.utils.requests.get")
    def test_successful_retrieval(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"id": {"id": "device-id-123"}, "name": "my-device"},
            ]
        }
        mock_get.return_value = mock_response

        device_id = retrieve_thingsboard_device_id("token", "customer-1", "my-device")

        self.assertEqual(device_id, "device-id-123")

    @patch("importing.utils.requests.get")
    def test_device_not_found(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"id": {"id": "device-id-123"}, "name": "other-device"},
            ]
        }
        mock_get.return_value = mock_response

        with self.assertRaisesRegex(Exception, "not found"):
            retrieve_thingsboard_device_id("token", "customer-1", "my-device")

    @patch("importing.utils.requests.get")
    def test_empty_device_list(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"data": []}
        mock_get.return_value = mock_response

        with self.assertRaisesRegex(Exception, "not found"):
            retrieve_thingsboard_device_id("token", "customer-1", "my-device")

    @patch("importing.utils.requests.get")
    def test_multiple_devices_warns_and_returns_first(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [
                {"id": {"id": "first-id"}, "name": "my-device"},
                {"id": {"id": "second-id"}, "name": "my-device"},
            ]
        }
        mock_get.return_value = mock_response

        with self.assertLogs("importing.utils", level="WARNING") as cm:
            device_id = retrieve_thingsboard_device_id(
                "token", "customer-1", "my-device"
            )

        self.assertEqual(device_id, "first-id")
        self.assertIn("found 2", cm.output[0])

    @patch("importing.utils.requests.get")
    def test_request_failure(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        with self.assertRaisesRegex(Exception, "Failed to retrieve devices"):
            retrieve_thingsboard_device_id("token", "customer-1", "my-device")

    @patch("importing.utils.requests.get")
    def test_auth_header_sent(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "data": [{"id": {"id": "dev-1"}, "name": "dev"}]
        }
        mock_get.return_value = mock_response

        retrieve_thingsboard_device_id("my-token", "cust-1", "dev")

        call_kwargs = mock_get.call_args[1]
        self.assertEqual(call_kwargs["headers"]["X-Authorization"], "Bearer my-token")


class RetrieveThingsboardDataTest(TestCase):
    """Tests for retrieve_thingsboard_data."""

    @patch("importing.utils.retrieve_thingsboard_device_id")
    @patch("importing.utils.requests.get")
    def test_successful_retrieval(self, mock_get, mock_device_id):
        mock_device_id.return_value = "device-id-123"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "temperature": [{"ts": 1000, "value": "25.5"}]
        }
        mock_get.return_value = mock_response

        result = retrieve_thingsboard_data(
            "token", "customer-1", "my-device", "temperature", 1000, 2000
        )

        self.assertEqual(result, {"temperature": [{"ts": 1000, "value": "25.5"}]})

    @patch("importing.utils.retrieve_thingsboard_device_id")
    @patch("importing.utils.requests.get")
    def test_request_failure(self, mock_get, mock_device_id):
        mock_device_id.return_value = "device-id-123"
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_get.return_value = mock_response

        with self.assertRaisesRegex(Exception, "Failed to retrieve data"):
            retrieve_thingsboard_data(
                "token", "customer-1", "my-device", "temperature", 1000, 2000
            )

    @patch("importing.utils.retrieve_thingsboard_device_id")
    @patch("importing.utils.requests.get")
    def test_delegates_to_device_id_lookup(self, mock_get, mock_device_id):
        mock_device_id.return_value = "dev-id"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        retrieve_thingsboard_data("tok", "cust-1", "my-device", "var", 100, 200)

        mock_device_id.assert_called_once_with("tok", "cust-1", "my-device")

    @patch("importing.utils.retrieve_thingsboard_device_id")
    @patch("importing.utils.requests.get")
    def test_auth_header_sent(self, mock_get, mock_device_id):
        mock_device_id.return_value = "dev-id"
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        retrieve_thingsboard_data("my-token", "cust-1", "my-device", "var", 100, 200)

        call_kwargs = mock_get.call_args[1]
        self.assertEqual(call_kwargs["headers"]["X-Authorization"], "Bearer my-token")

    @patch("importing.utils.retrieve_thingsboard_device_id")
    def test_device_lookup_failure_propagates(self, mock_device_id):
        mock_device_id.side_effect = Exception("Device 'x' not found!")

        with self.assertRaisesRegex(Exception, "not found"):
            retrieve_thingsboard_data(
                "token", "customer-1", "x", "temperature", 1000, 2000
            )
