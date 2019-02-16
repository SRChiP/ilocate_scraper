import logging
from datetime import datetime, timedelta

from ilocate.transformer import filter_api_data, dict_to_record_objects

log = logging.getLogger(__name__)


class Runner(object):

    def __init__(self, api, persistence):
        self.api = api
        self.persistence = persistence

    def find_oldest_record(self, history_to_check=60, today=None):
        """Use bisect algorithm to find the oldest available record"""
        self.api.login()
        # Today is mostly used for debug purposes
        if not today:
            today = datetime.today().date()
        lo = -history_to_check
        hi = 0
        count = 1
        while lo < hi:
            mid = (lo + hi) // 2
            log.debug("Checking date %s", today + timedelta(days=mid))
            if self._check_date_valid(today + timedelta(days=mid)):
                hi = mid
            else:
                lo = mid + 1
            log.debug("Loop count: %s", count)
            count += 1
        log.debug("Date %s was chosen as oldest record", today + timedelta(days=lo))
        return (today + timedelta(days=lo)).date()

    def _check_date_valid(self, date):
        data = self.api.get_data(date)
        log.debug("Date %s is %s", date, 'valid' if bool(data) else 'invalid')
        return bool(data)

    def retrieve_and_save_single_day(self, date):

        self.api.login()
        self.api.get_recent_data()  # To check that the API works
        history_data = self.api.get_data(date)
        filtered_data = filter_api_data(history_data)

        for data_item in filtered_data:
            db_rec = dict_to_record_objects(data_item)
            self.persistence.add_record(db_rec)

    def retrieve_and_save_date_range(self, date1, date2):

        self.api.login()
        self.api.get_recent_data()  # To check that the API works
        history_data = self.api.get_data_range(date1, date2)
        filtered_data = filter_api_data(history_data)
        log.debug("Have %s records to commit", len(filtered_data))

        batch = []
        batch_count = 0
        for data_item in filtered_data:
            db_rec = dict_to_record_objects(data_item)
            batch.append(db_rec)

            if len(batch) >= 100:
                self.persistence.add_record(batch)
                self.persistence.commit()
                batch_count += len(batch)
                batch.clear()
                log.debug("Added %s records total", batch_count)

        self.persistence.add_record(batch)
        self.persistence.commit()
        batch_count += len(batch)
        log.debug("Added %s records total", batch_count)

    def daily_update(self):
        log.info("Running the daily update")
        latest_old = self.persistence.latest_record_datetime
        latest_old += timedelta(seconds=1)
        self.retrieve_and_save_date_range(latest_old, datetime.today())
