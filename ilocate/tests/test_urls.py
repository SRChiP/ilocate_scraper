from ilocate import urls
import unittest
import mock

class APITest(unittest.TestCase):

    @mock.patch("urls")
    def test_api(self):
        i = 33
        urls
        pass