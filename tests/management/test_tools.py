from unittest.mock import MagicMock, patch

import requests
from django.test import TestCase

from management.tools import (
    retrieve_thingsboard_customerid,
    thingsboard_token_generator,
)


class ThingsboardTokenGeneratorTest(TestCase):
    """Tests for thingsboard_token_generator."""

    @patch("management.tools.requests.post")
    def test_successful_authentication(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"token": "test-token-123"}
        mock_post.return_value = mock_response

        token = thingsboard_token_generator("user@example.com", "password123")

        self.assertEqual(token, "test-token-123")
        mock_post.assert_called_once()
        call_args = mock_post.call_args
        self.assertIn("api/auth/login", call_args[0][0])

    @patch("management.tools.requests.post")
    def test_auth_failure_status_code(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.text = "Unauthorized"
        mock_post.return_value = mock_response

        with self.assertRaisesRegex(Exception, "Failed to authenticate"):
            thingsboard_token_generator("user@example.com", "wrong-password")

    @patch("management.tools.requests.post")
    def test_missing_token_in_response(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = '{"refreshToken": "something"}'
        mock_post.return_value = mock_response

        with self.assertRaisesRegex(Exception, "Token not found"):
            thingsboard_token_generator("user@example.com", "password123")

    @patch("management.tools.requests.post")
    def test_request_exception(self, mock_post):
        mock_post.side_effect = requests.RequestException("Connection refused")

        with self.assertRaisesRegex(Exception, "Failed to authenticate"):
            thingsboard_token_generator("user@example.com", "password123")

    @patch("management.tools.settings")
    def test_tb_host_not_set(self, mock_settings):
        mock_settings.TB_HOST = None

        with self.assertRaisesRegex(
            Exception, "TB_HOST environment variable is not set"
        ):
            thingsboard_token_generator("user@example.com", "password123")

    @patch("management.tools.requests.post")
    def test_uses_timeout(self, mock_post):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"token": "test-token"}
        mock_post.return_value = mock_response

        thingsboard_token_generator("user@example.com", "password123")

        call_kwargs = mock_post.call_args[1]
        self.assertIn("timeout", call_kwargs)


class RetrieveThingsboardCustomerIdTest(TestCase):
    """Tests for retrieve_thingsboard_customerid."""

    @patch("management.tools.requests.get")
    def test_successful_retrieval(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"customerId": {"id": "customer-id-abc-123"}}
        mock_get.return_value = mock_response

        customer_id = retrieve_thingsboard_customerid("valid-token")

        self.assertEqual(customer_id, "customer-id-abc-123")
        mock_get.assert_called_once()
        call_args = mock_get.call_args
        self.assertIn("api/auth/user", call_args[0][0])

    @patch("management.tools.requests.get")
    def test_auth_header_sent(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"customerId": {"id": "cid"}}
        mock_get.return_value = mock_response

        retrieve_thingsboard_customerid("my-token")

        call_kwargs = mock_get.call_args[1]
        self.assertEqual(call_kwargs["headers"]["X-Authorization"], "Bearer my-token")

    @patch("management.tools.requests.get")
    def test_failure_status_code(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 403
        mock_response.text = "Forbidden"
        mock_get.return_value = mock_response

        with self.assertRaisesRegex(Exception, "Failed to retrieve user info"):
            retrieve_thingsboard_customerid("expired-token")

    @patch("management.tools.requests.get")
    def test_request_exception(self, mock_get):
        mock_get.side_effect = requests.RequestException("Timeout")

        with self.assertRaisesRegex(Exception, "Failed to retrieve user info"):
            retrieve_thingsboard_customerid("valid-token")

    @patch("management.tools.settings")
    def test_tb_host_not_set(self, mock_settings):
        mock_settings.TB_HOST = None

        with self.assertRaisesRegex(
            Exception, "TB_HOST environment variable is not set"
        ):
            retrieve_thingsboard_customerid("valid-token")

    @patch("management.tools.requests.get")
    def test_missing_customer_id_returns_none(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_get.return_value = mock_response

        customer_id = retrieve_thingsboard_customerid("valid-token")

        self.assertIsNone(customer_id)

    @patch("management.tools.requests.get")
    def test_uses_timeout(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"customerId": {"id": "cid"}}
        mock_get.return_value = mock_response

        retrieve_thingsboard_customerid("valid-token")

        call_kwargs = mock_get.call_args[1]
        self.assertIn("timeout", call_kwargs)
