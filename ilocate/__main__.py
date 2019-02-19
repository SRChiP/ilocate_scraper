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
        oldest_rec_date = runner.find_oldest_record(120)
        runner.retrieve_and_save_date_range(datetime.combine(oldest_rec_date, datetime.min.time()), datetime.today())
    else:
        runner.daily_update()


if __name__ == "__main__":
    main()
