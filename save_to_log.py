import requests
from datetime import datetime
import pytz
import re

from api import IlocateAPI
from db import Persistence, RECORD
from transformer import transform_data
from urls import DialogURLs
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

api = IlocateAPI(config['login']['usernumber'], config['login']['password'])
persistence = Persistence()

def get_data(date):

    login = api.login()
    getd = api.get_recent_data()
    history_data = api.get_data(date)
    # print(his.json())

    return transform_data(history_data)


def get_data_rg(date1, date2):

    login = api.login()
    getd = api.get_recent_data()
    history_data = api.get_data_range(date1, date2)
    # print(his.json())

    return transform_data(history_data)

if __name__ == "__main__":

    # history = get_data("2017-10-4")
    last_record = persistence.latest_record_datetime
    history2 = get_data_rg(datetime(2017, 9, 20), datetime.today())
    # print(history)

    for data in history2:
        db_rec = RECORD(speed=data['speed'], dist_from_last=data['dist_from_last'], device_state=data['state'],
                        lat=data['lat'], lon=data['lon'], time_from_last=data['time_from_last'], timestamp=data['timestamp'],
                        date=data['date'], time=data['time'], dt=data['datetime'])
        persistence.add_record(db_rec)

"""{'speed': 0, 'dist_from_last': 0, 'state': 'on', 'lon': '7.8890638', 'time_from_last': 0,
'nic': None, 'lat': '7.0597020', 'timestamp': 1467524518, 'device_type': '9', 'charge_status': '1', 'id': '1518',
'number': '77xxxxxxx', 'time_st': 'July 3, 2016, 11:11 AM', 'error': False, 'update_type': '2', 'name': 'XXX-0000'}"""
