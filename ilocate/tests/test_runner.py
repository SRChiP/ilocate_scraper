import unittest
from datetime import datetime, timedelta, date
from unittest.mock import Mock, patch, PropertyMock

from ilocate.runner import Runner


class TestRunner(unittest.TestCase):

    @classmethod
    def setUpClass(cls):

        @staticmethod
        def date_data(dt):
            """Function to serve the preset data based on the input date"""
            if dt.date() == date(2018, 11, 6):
                return [
                    {
                        'lon': '79.8887663', 'time_st': 'November 6, 2018, 06:12:58 PM', 'timestamp': 1541508178,
                        'dist_from_last': 0, 'id': '1518', 'error': False, 'speed': 0, 'time_from_last': 0, 'device_type': '9',
                        'nic': None, 'charge_status': '1', 'number': '778352958', 'lat': '7.0598198', 'name': 'CAE-6745',
                        'update_type': '2', 'state': 'on'
                    },
                    {
                        'lon': '79.8893412', 'time_st': 'November 6, 2018, 06:15:59 PM', 'timestamp': 1541508359,
                        'dist_from_last': 0.06556343164903, 'id': '1518', 'error': False, 'speed': 1.3040240548978,
                        'time_from_last': 181, 'device_type': '9', 'nic': None, 'charge_status': '1', 'number': '778352958',
                        'lat': '7.0596710', 'name': 'CAE-6745', 'update_type': '2', 'state': 'on'
                    },
                ]
            elif dt.date() == date(2018, 11, 5):
                return [
                    {
                        'lon': '79.8887663', 'time_st': 'November 5, 2018, 01:12:00 AM', 'timestamp': 1541360520,
                        'dist_from_last': 0, 'id': '1518', 'error': False, 'speed': 0, 'time_from_last': 0,
                        'device_type': '9',
                        'nic': None, 'charge_status': '1', 'number': '778352958', 'lat': '7.0598198',
                        'name': 'CAE-6745',
                        'update_type': '2', 'state': 'on'
                    },
                ]
            else:
                return None
        cls.date_data = date_data

    def setUp(self):
        api = Mock()
        api.get_data = Mock(side_effect=self.date_data)
        persistence = Mock()
        self.yesterday = datetime.now() - timedelta(days=1)
        type(persistence).latest_record_datetime = PropertyMock(return_value=self.yesterday)

        self.runner = Runner(api, persistence)

    def test_find_oldest_record(self):
        oldest_record = self.runner.find_oldest_record(5, today=datetime(2018, 11, 6))
        self.assertEqual(date(2018, 11, 5), oldest_record)


    @patch('ilocate.runner.dict_to_record_objects')
    def test_retrieve_and_save_single_day(self, dict_to_rec):
        self.runner.retrieve_and_save_single_day(datetime(2018, 11, 6))
        self.assertEqual(dict_to_rec.call_count, 2)
        self.assertEqual(self.runner.persistence.add_record.call_count, 2)
        self.assertGreaterEqual(self.runner.api.login.call_count, 1)

    def test_save_date_range(self):
        raise NotImplementedError

    @patch('ilocate.runner.Runner.retrieve_and_save_date_range')
    def test_daily_update(self, save_date_range_mock):
        self.runner.daily_update()
        start, end = save_date_range_mock.call_args[0]
        self.assertGreater(start, self.yesterday)
        self.assertLessEqual(end, datetime.now())


if __name__ == '__main__':
    unittest.main()
