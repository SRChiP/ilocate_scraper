import unittest
from mock import Mock
from ilocate.utils import retry


class TestUtils(unittest.TestCase):

    def test_retry_tries(self):
        error_function = Mock(side_effect=KeyError())
        login_mock = Mock()

        @retry(tries=3)
        def try_logic(this):
            error_function()

        with self.assertRaises(KeyError):
            try_logic(login_mock)
        self.assertEqual(error_function.call_count, 3)


if __name__ == '__main__':
    unittest.main()
