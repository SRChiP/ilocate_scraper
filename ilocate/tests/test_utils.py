import unittest

import time
from unittest.mock import Mock

from ilocate.utils import retry


class TestUtils(unittest.TestCase):

    def setUp(self):
        self.error_function = Mock(side_effect=KeyError())
        self.login_mock = Mock()  # In order to stub the self.login function in the API

    def test_retry_tries(self):

        @retry(tries=3)
        def try_logic(this):
            self.error_function()

        with self.assertRaises(KeyError):
            try_logic(self.login_mock)
        self.assertEqual(self.error_function.call_count, 3)

    def test_retry_delay(self):
        self._retry_check(tries=2, delay=1, backoff=2, expected=3)
        self._retry_check(tries=3, delay=1, backoff=2, expected=7)
        self._retry_check(tries=2, delay=2, backoff=2, expected=6)
        self._retry_check(tries=2, delay=1, backoff=3, expected=4)
        self._retry_check(tries=2, delay=0.5, backoff=4, expected=2.5)

    def _retry_check(self, tries, delay, backoff, expected):
        start_time = time.perf_counter()

        @retry(tries=tries, delay=delay, backoff=backoff)
        def try_logic(this):
            self.error_function()

        with self.assertRaises(KeyError):
            try_logic(self.login_mock)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        # Check that the time is between +/- 1 second
        self.assertGreaterEqual(total_time, expected-1)
        self.assertLessEqual(total_time, expected+1)


if __name__ == '__main__':
    unittest.main()
