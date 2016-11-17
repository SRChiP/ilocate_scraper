import re

from datetime import datetime

import pytz

zero_pad_date = re.compile(r'(^\D+) (\d)(, )')
keys_to_keep = {'speed', 'dist_from_last', 'state', 'lon', 'time_from_last', 'lat', 'time_st', 'number'}


def transform_data(input_data):
    parsed_history_data = []

    for data in input_data:
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
