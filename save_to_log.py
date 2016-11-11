import requests
from datetime import datetime
import pytz
import re
from db import Persistence, RECORD
from urls import DialogURLs
import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def get_data(date):

    s = requests.session()
    login = s.post(**DialogURLs.login_url(config['login']['usernumber'], config['login']['password']))
    getd = s.post(**DialogURLs.current_url())
    # print(getd.json())
    his = s.post(**DialogURLs.history_url(config['login']['carnumber'], date))
    # print(his.json())
    history_json = his.json()

    history_data = history_json['data']

    # Remove keys
    keys_to_keep = {'speed', 'dist_from_last', 'state', 'lon', 'time_from_last', 'lat', 'time_st'}

    parsed_history_data = []
    # The date should be zero-padded to convert into an DateTime object.
    zero_pad_date = re.compile(r'(^\D+) (\d)(, )')
    for data in history_data:
        new_dict = {k: v for k, v in data.items() if k in keys_to_keep}
        # Do the actual zero-padding. "10 5, 2016" --> "10 05, 2016".
        new_date = datetime.strptime(zero_pad_date.sub(r'\1 0\2\3', new_dict['time_st']), '%B %d, %Y, %I:%M:%S %p')
        new_date = new_date.replace(tzinfo=pytz.timezone("Asia/Colombo"))
        new_dict['date'] = new_date.date()
        new_dict['time'] = new_date.time()
        new_dict['datetime'] = new_date
        new_dict['timestamp'] = new_date.timestamp()
        parsed_history_data.append(new_dict)
    return parsed_history_data

history = get_data("2016-10-25")
# print(history)


persistence = Persistence()
for data in history:
    db_rec = RECORD(speed=data['speed'], dist_from_last=data['dist_from_last'], device_state=data['state'],
                    lat=data['lat'], lon=data['lon'], time_from_last=data['time_from_last'], timestamp=data['timestamp'],
                    date=data['date'], time=data['time'], dt=data['datetime'])
    persistence.add_record(db_rec)

"""{'speed': 0, 'dist_from_last': 0, 'state': 'on', 'lon': '7.8890638', 'time_from_last': 0,
'nic': None, 'lat': '7.0597020', 'timestamp': 1467524518, 'device_type': '9', 'charge_status': '1', 'id': '1518',
'number': '77xxxxxxx', 'time_st': 'July 3, 2016, 11:11 AM', 'error': False, 'update_type': '2', 'name': 'XXX-0000'}"""
