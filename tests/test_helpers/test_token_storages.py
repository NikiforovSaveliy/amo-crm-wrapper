from unittest import TestCase

from amopy.helpers.token_storages import LongTermTokenStorage


class TestLongTermTokenStorage(TestCase):

    def setUp(self):
        self.token = "test_token"
        self.storage = LongTermTokenStorage(self.token)

    def test_get_access_token(self):
        self.assertEqual(self.storage.get_access_token(), self.token)

    def test_get_auth_header(self):
        expected_header = {"Authentication": "Bearer " + self.token}
        self.assertEqual(self.storage.get_auth_header(), expected_header)
