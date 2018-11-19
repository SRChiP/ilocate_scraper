import unittest

from datetime import date, datetime, time
from mock import Mock
import pytz
from ilocate.transformer import filter_api_data
from ilocate.utils import retry


class TestUtils(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.input_payload = [
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
            {
                'lon': '79.8890092', 'time_st': 'November 6, 2018, 06:20:58 PM', 'timestamp': 1541508658,
                'dist_from_last': 0.036651430567261, 'id': '1518', 'error': False, 'speed': 0.44128812723124,
                'time_from_last': 299, 'device_type': '9', 'nic': None, 'charge_status': '1', 'number': '778352958',
                'lat': '7.0596617', 'name': 'CAE-6745', 'update_type': '2', 'state': 'on'
            },
            {
                'lon': '79.8892383', 'time_st': 'November 8, 2018, 05:07:57 PM', 'timestamp': 1541677077,
                'dist_from_last': 0, 'id': '1518', 'error': False, 'speed': 0, 'time_from_last': 0,
                'device_type': '9', 'nic': None, 'charge_status': '1', 'number': '778352958', 'lat': '7.0597770',
                'name': 'CAE-6745', 'update_type': '2', 'state': 'on'
            }
        ]

    @staticmethod
    def _dict_compare(d1: dict, d2: dict) -> tuple:
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        intersect_keys = d1_keys.intersection(d2_keys)
        added = d1_keys - d2_keys
        removed = d2_keys - d1_keys
        modified = {o: (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
        same = set(o for o in intersect_keys if d1[o] == d2[o])
        return added, removed, modified, same

    def test_filter_api_data(self):
        output = filter_api_data(self.input_payload)
        local_tz = pytz.timezone('Asia/Colombo')
        expected_value = [
            {
                # 'lon': '79.8887663', 'time_st': 'November 6, 2018, 06:12:58 PM', 'timestamp': 1541508178,
                # 'dist_from_last': 0, 'id': '1518', 'error': False, 'speed': 0, 'time_from_last': 0, 'device_type': '9',
                # 'nic': None, 'charge_status': '1', 'number': '778352958', 'lat': '7.0598198', 'name': 'CAE-6745',
                # 'update_type': '2', 'state': 'on',
                'lon': '79.8887663', 'time_st': 'November 6, 2018, 06:12:58 PM', 'timestamp': 1541508178.0,
                'dist_from_last': 0, 'speed': 0, 'time_from_last': 0, 'number': '778352958', 'lat': '7.0598198',
                'state': 'on', 'date': date(2018, 11, 6), 'time': time(18, 12, 58),
                'datetime': local_tz.localize(datetime(2018, 11, 6, 18, 12, 58))
            },
            {
                # 'lon': '79.8893412', 'time_st': 'November 6, 2018, 06:15:59 PM', 'timestamp': 1541508359,
                # 'dist_from_last': 0.06556343164903, 'id': '1518', 'error': False, 'speed': 1.3040240548978,
                # 'time_from_last': 181, 'device_type': '9', 'nic': None, 'charge_status': '1', 'number': '778352958',
                # 'lat': '7.0596710', 'name': 'CAE-6745', 'update_type': '2', 'state': 'on',

                'lon': '79.8893412', 'time_st': 'November 6, 2018, 06:15:59 PM', 'timestamp': 1541508359.0,
                'dist_from_last': 0.06556343164903, 'speed': 1.3040240548978, 'time_from_last': 181,
                'number': '778352958', 'lat': '7.0596710', 'state': 'on', 'date': date(2018, 11, 6),
                'time': time(18, 15, 59),
                'datetime': local_tz.localize(datetime(2018, 11, 6, 18, 15, 59))
            },
            {
                # 'lon': '79.8890092', 'time_st': 'November 6, 2018, 06:20:58 PM', 'timestamp': 1541508658,
                # 'dist_from_last': 0.036651430567261, 'id': '1518', 'error': False, 'speed': 0.44128812723124,
                # 'time_from_last': 299, 'device_type': '9', 'nic': None, 'charge_status': '1', 'number': '778352958',
                # 'lat': '7.0596617', 'name': 'CAE-6745', 'update_type': '2', 'state': 'on',

                'lon': '79.8890092', 'time_st': 'November 6, 2018, 06:20:58 PM', 'timestamp': 1541508658.0,
                'dist_from_last': 0.036651430567261, 'speed': 0.44128812723124, 'time_from_last': 299,
                'number': '778352958', 'lat': '7.0596617', 'state': 'on', 'date': date(2018, 11, 6),
                'time': time(18, 20, 58),
                'datetime': local_tz.localize(datetime(2018, 11, 6, 18, 20, 58))
            },
            {
                # 'lon': '79.8892383', 'time_st': 'November 8, 2018, 05:07:57 PM', 'timestamp': 1541677077,
                # 'dist_from_last': 0, 'id': '1518', 'error': False, 'speed': 0, 'time_from_last': 0,
                # 'device_type': '9', 'nic': None, 'charge_status': '1', 'number': '778352958', 'lat': '7.0597770',
                # 'name': 'CAE-6745', 'update_type': '2', 'state': 'on',

                'lon': '79.8892383', 'time_st': 'November 8, 2018, 05:07:57 PM', 'timestamp': 1541677077.0,
                'dist_from_last': 0, 'speed': 0, 'time_from_last': 0, 'number': '778352958', 'lat': '7.0597770',
                'state': 'on', 'date': date(2018, 11, 8), 'time': time(17, 7, 57),
                'datetime': local_tz.localize(datetime(2018, 11, 8, 17, 7, 57))
            }
        ]
        for x in range(4):
            added, removed, modified, same = self._dict_compare(expected_value[x], output[x])
            self.assertLess(len(added), 1, added)
            self.assertLess(len(removed), 1, removed)
            self.assertLess(len(modified), 1, modified)
            self.assertEqual(len(same), len(output[x]))


if __name__ == '__main__':
    unittest.main()


