import requests
from datetime import datetime
import pytz
import re

from ilocate.api import IlocateAPI
from ilocate.db import Persistence, RECORD
from ilocate.transformer import transform_data
from ilocate.urls import DialogURLs
import configparser

config = configparser.ConfigParser()
config.read(["config.ini", "../config.ini"])

api = IlocateAPI(config['login']['usernumber'], config['login']['password'])
persistence = Persistence()


def get_data(date):

    login = api.login()
    getd = api.get_recent_data()
    history_data = api.get_data(date)
    # print(his.json())

    return transform_data(history_data)


def get_data_rg(date1, date2):

    api.login()
    getd = api.get_recent_data()
    history_data = api.get_data_range(date1, date2)
    # print(his.json())

    return transform_data(history_data)
