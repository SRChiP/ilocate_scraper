import requests
from datetime import datetime
import pytz
import re

from ilocate.api import IlocateAPI
from ilocate.db import Persistence, RECORD
from ilocate.transformer import filter_api_data, dict_to_record_objects
from ilocate.urls import DialogURLs
import configparser

config = configparser.ConfigParser()
config.read(["config.ini", "../config.ini"])

api = IlocateAPI(config['login']['usernumber'], config['login']['password'])
persistence = Persistence()


class Runner(object):

    def __init__(self, api, persistence):
        self.api = api
        self.persistence = persistence


    def retrieve_and_save_single_day(self, date):

        self.api.login()
        self.api.get_recent_data()  # To check that the API works
        history_data = api.get_data(date)
        filtered_data = filter_api_data(history_data)

        for data_item in filtered_data:
            db_rec = dict_to_record_objects(data_item)
            persistence.add_record(db_rec)

    def retrieve_and_save_date_range(self, date1, date2):

        self.api.login()
        self.api.get_recent_data()  # To check that the API works
        history_data = api.get_data_range(date1, date2)
        filtered_data = filter_api_data(history_data)

        for data_item in filtered_data:
            db_rec = dict_to_record_objects(data_item)
            persistence.add_record(db_rec)
