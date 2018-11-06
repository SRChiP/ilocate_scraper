# -*- coding: utf-8 -*-
import configparser
import sys
from datetime import datetime

from ilocate.api import IlocateAPI
from ilocate.db import Persistence
from ilocate.runner import Runner

import logging


def main():
    """Main routine of ilocate."""
    logging.basicConfig(
        level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        stream=sys.stdout)

    logging.info('iLocate Scraper Started')

    logging.info("Reading the config.")
    config = configparser.ConfigParser()
    config.read(["config.ini", "../config.ini"])
    logging.debug("Config loaded")

    api = IlocateAPI(config['login']['usernumber'], config['login']['password'])
    logging.info("API configured with user: %s", api.usernumber)
    persistence = Persistence()

    runner = Runner(api, persistence)
    last_record = persistence.latest_record_datetime
    if not last_record:
        oldest_rec = runner.find_oldest_record(120)
        runner.retrieve_and_save_date_range(oldest_rec, datetime.today())
    else:
        runner.daily_update()

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
