import requests
from datetime import datetime
import pytz
import re
import sqlalchemy

import configparser

config = configparser.ConfigParser()
config.read("config.ini")


def get_data(date):
    post_data = {
        "login": {"LoginForm[username]": config['login']['usernumber'],
                  "LoginForm[password]": config['login']['password']},
        "history": {"number": config['login']['carnumber'], "start_time": "12:00:00 AM", "end_time": "11:59:59 PM",
                    "date": date}
    }

    params = {
        "login": {"r": 'site/login'},
        "current": {"r": "/iLocateWeb/location/getCurrentData"},
        "history": {"r": "/iLocateWeb/location/getHistoryData"}
    }
    s = requests.session()
    login = s.post("http://locate.dialog.lk/web/index.php", post_data['login'], params=params['login'])
    # getd = s.post("http://locate.dialog.lk/web/index.php", params=params['current'])
    # print(getd.json())
    his = s.post("http://locate.dialog.lk/web/index.php", post_data['history'], params=params['history'])
    # print(his.json())
    history_json = his.json()
    history_data = history_json['data']

    # Remove keys
    keys_to_keep = {'speed', 'dist_from_last', 'state', 'lon', 'time_from_last', 'lat', 'time_st'}

    parsed_history_data = []
    zero_pad_date = re.compile(r'(^\D+) (\d)(, )')
    for data in history_data:
        new_dict = {k: v for k, v in data.items() if k in keys_to_keep}
        new_date = datetime.strptime(zero_pad_date.sub(r'\1 0\2\3', new_dict['time_st']), '%B %d, %Y, %I:%M:%S %p')
        new_date = new_date.replace(tzinfo=pytz.timezone("Asia/Colombo"))
        new_dict['date'] = new_date.date()
        new_dict['time'] = new_date.time()
        new_dict['timestamp'] = new_date.timestamp()
        parsed_history_data.append(new_dict)
    return parsed_history_data

history = get_data("2016-7-3")
print(history)


"""{'speed': 0, 'dist_from_last': 0, 'state': 'on', 'lon': '7.8890638', 'time_from_last': 0,
'nic': None, 'lat': '7.0597020', 'timestamp': 1467524518, 'device_type': '9', 'charge_status': '1', 'id': '1518',
'number': '77xxxxxxx', 'time_st': 'July 3, 2016, 11:11 AM', 'error': False, 'update_type': '2', 'name': 'XXX-0000'}"""