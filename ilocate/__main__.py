
# -*- coding: utf-8 -*-
import configparser
from datetime import datetime

from ilocate.api import IlocateAPI
from ilocate.db import Persistence, RECORD
from ilocate.runner import Runner


def main():
    """Main routine of ilocate."""
    # history = get_data("2017-10-4")

    config = configparser.ConfigParser()
    config.read(["config.ini", "../config.ini"])

    api = IlocateAPI(config['login']['usernumber'], config['login']['password'])
    persistence = Persistence()

    runner = Runner(api, persistence)
    last_record = persistence.latest_record_datetime
    runner.find_oldest_record(365)
    runner.retrieve_and_save_date_range(datetime(2018, 11, 3), datetime.today())
    # print(history)

    """{'speed': 0, 'dist_from_last': 0, 'state': 'on', 'lon': '7.8890638', 'time_from_last': 0,
    'nic': None, 'lat': '7.0597020', 'timestamp': 1467524518, 'device_type': '9', 'charge_status': '1', 'id': '1518',
    'number': '77xxxxxxx', 'time_st': 'July 3, 2016, 11:11 AM', 'error': False, 'update_type': '2', 'name': 'XXX-0000'}"""

    # Read config
    # Check if first
    # If first, find earliest
    ## get data from earliest to now
    # If not first
    ## Get data from last to now
    # Exit


if __name__ == "__main__":
    main()

