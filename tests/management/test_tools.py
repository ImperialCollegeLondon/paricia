import json
from unittest.mock import Mock, patch

import requests
from django.test import SimpleTestCase

from management import tools


class TestThingsboardTools(SimpleTestCase):
    def test_thingsboard_token_generator_uses_timeout(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"token": "generated_token"}
        mock_response.text = ""

        with (
            patch("management.tools.os.getenv", return_value="tb.example.com"),
            patch(
                "management.tools.requests.post", return_value=mock_response
            ) as mock_post,
        ):
            token = tools.thingsboard_token_generator("tb_user", "tb_pass")

        self.assertEqual(token, "generated_token")
        mock_post.assert_called_once_with(
            "https://tb.example.com/api/auth/login",
            headers={"Content-Type": "application/json", "Accept": "application/json"},
            data=json.dumps({"username": "tb_user", "password": "tb_pass"}),
            timeout=tools.THINGSBOARD_REQUEST_TIMEOUT,
        )

    def test_thingsboard_token_generator_wraps_request_exception(self):
        with (
            patch("management.tools.os.getenv", return_value="tb.example.com"),
            patch(
                "management.tools.requests.post",
                side_effect=requests.Timeout("connect timed out"),
            ),
        ):
            with self.assertRaises(Exception) as exc:
                tools.thingsboard_token_generator("tb_user", "tb_pass")

        self.assertIn("Failed to authenticate with Thingsboard API", str(exc.exception))
        self.assertIn("connect timed out", str(exc.exception))

    def test_retrieve_thingsboard_customerid_uses_timeout(self):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"customerId": {"id": "customer_123"}}
        mock_response.text = ""

        with (
            patch("management.tools.os.getenv", return_value="tb.example.com"),
            patch(
                "management.tools.requests.get", return_value=mock_response
            ) as mock_get,
        ):
            customer_id = tools.retrieve_thingsboard_customerid("access_token_abc")

        self.assertEqual(customer_id, "customer_123")
        mock_get.assert_called_once_with(
            "https://tb.example.com/api/auth/user",
            headers={"X-Authorization": "Bearer access_token_abc"},
            timeout=tools.THINGSBOARD_REQUEST_TIMEOUT,
        )

    def test_retrieve_thingsboard_customerid_wraps_request_exception(self):
        with (
            patch("management.tools.os.getenv", return_value="tb.example.com"),
            patch(
                "management.tools.requests.get",
                side_effect=requests.ConnectionError("host unreachable"),
            ),
        ):
            with self.assertRaises(Exception) as exc:
                tools.retrieve_thingsboard_customerid("access_token_abc")

        self.assertIn(
            "Failed to retrieve user info from Thingsboard", str(exc.exception)
        )
        self.assertIn("host unreachable", str(exc.exception))
