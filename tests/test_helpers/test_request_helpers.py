import json
import unittest
from unittest.mock import Mock, patch
from urllib.error import HTTPError, URLError

from amopy.helpers.request_helpers import (
    UrlLibRequestHelper,
    InvalidResponseStatusError,
)


class MockTokenStorage:

    def get_auth_header(self):
        return {"Authorization": "Bearer mock_token"}


class TestUrlLibRequestHelper(unittest.TestCase):

    def setUp(self):
        self.base_url = "https://api.example.com"
        self.token_storage = MockTokenStorage()
        self.helper = UrlLibRequestHelper(self.base_url, self.token_storage)

    @patch("urllib.request.urlopen")
    def test_get_url(self, mock_urlopen):
        url_with_params = self.helper.get_url("test/path", {"key": "value"})
        url_without_params = self.helper.get_url("test/path")

        self.assertEqual(url_with_params, "https://api.example.com/test/path?key=value")
        self.assertEqual(url_without_params, "https://api.example.com/test/path")

    @patch("urllib.request.urlopen")
    def test_get_request(self, mock_urlopen):
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"success": True}).encode()
        mock_urlopen.return_value = mock_response
        mock_response.getcode.return_value = 200

        response = self.helper.get("test/path")

        self.assertEqual(response, {"success": True})

        mock_urlopen.assert_called_once()
        args, kwargs = mock_urlopen.call_args
        self.assertEqual(args[0].method, "GET")

    @patch("urllib.request.urlopen")
    def test_post_request(self, mock_urlopen):
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"created": True}).encode()
        mock_urlopen.return_value = mock_response
        mock_response.getcode.return_value = 200

        response = self.helper.post("test/path", data={"name": "example"})

        self.assertEqual(response, {"created": True})

        mock_urlopen.assert_called_once()
        args, kwargs = mock_urlopen.call_args
        self.assertEqual(args[0].method, "POST")

    @patch("urllib.request.urlopen")
    def test_patch_request(self, mock_urlopen):
        mock_response = Mock()
        mock_response.read.return_value = json.dumps({"updated": True}).encode()
        mock_response.getcode.return_value = 200
        mock_urlopen.return_value = mock_response

        response = self.helper.patch("test/path", data={"name": "new_name"})

        self.assertEqual(response, {"updated": True})

        mock_urlopen.assert_called_once()
        args, kwargs = mock_urlopen.call_args
        self.assertEqual(args[0].method, "PATCH")

    @patch("urllib.request.urlopen")
    def test_request_raises_error_on_http_error(self, mock_urlopen):
        mock_urlopen.side_effect = HTTPError(
            url="https://api.example.com/test/path",
            code=503,
            msg="Service Unavailable",
            hdrs=None,
            fp=None,
        )

        with self.assertRaises(InvalidResponseStatusError) as cm:
            self.helper.get("test/path", headers={})
        self.assertIn("Error occurred during making request", str(cm.exception))

    @patch("urllib.request.urlopen")
    def test_request_raises_error_on_url_error(self, mock_urlopen):
        mock_urlopen.side_effect = URLError("Temporary failure in name resolution")

        with self.assertRaises(InvalidResponseStatusError) as cm:
            self.helper.get("test/path", headers={})
        self.assertIn("Error occurred during makingg request", str(cm.exception))

    @patch("urllib.request.urlopen")
    def test_request_raises_error_on_json_decode_error(self, mock_urlopen):
        mock_response = Mock()
        mock_response.getcode.return_value = 200
        mock_response.read.return_value = b"Invalid JSON"
        mock_urlopen.return_value = mock_response

        with self.assertRaises(InvalidResponseStatusError) as cm:
            self.helper.get("test/path", headers={})
        self.assertIn("Error occurred during decoding request body", str(cm.exception))


if __name__ == "__main__":
    unittest.main()
