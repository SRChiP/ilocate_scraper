import re
from datetime import datetime

import pytz

from ilocate.db import RECORD

zero_pad_date = re.compile(r'(^\D+) (\d)(, )')
keys_to_keep = {'speed', 'dist_from_last', 'state', 'lon', 'time_from_last', 'lat', 'time_st', 'number'}


def filter_api_data(api_data):
    """Take the API json response data and fix the data-types"""
    parsed_history_data = []

    for data in api_data:
        new_dict = {k: v for k, v in data.items() if k in keys_to_keep}
        # The date should be zero-padded to convert into an DateTime object.. "10 5, 2016" --> "10 05, 2016".
        new_date = datetime.strptime(zero_pad_date.sub(r'\1 0\2\3', new_dict['time_st']), '%B %d, %Y, %I:%M:%S %p')
        new_date = new_date.replace(tzinfo=pytz.timezone("Asia/Colombo"))
        new_dict['date'] = new_date.date()
        new_dict['time'] = new_date.time()
        new_dict['datetime'] = new_date  # saved without timezone
        new_dict['timestamp'] = new_date.timestamp()
        parsed_history_data.append(new_dict)

    return parsed_history_data


def dict_to_record_objects(single_record_dict):
    """Return a RECORD query object that can be added to the database"""
    return RECORD(speed=single_record_dict['speed'],
                  dist_from_last=single_record_dict['dist_from_last'],
                  device_state=single_record_dict['state'],
                  lat=single_record_dict['lat'], lon=single_record_dict['lon'],
                  time_from_last=single_record_dict['time_from_last'],
                  timestamp=single_record_dict['timestamp'],
                  date=single_record_dict['date'], time=single_record_dict['time'],
                  dt=single_record_dict['datetime'])

