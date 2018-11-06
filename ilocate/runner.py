from datetime import datetime, timedelta

from ilocate.transformer import filter_api_data, dict_to_record_objects


class Runner(object):

    def __init__(self, api, persistence):
        self.api = api
        self.persistence = persistence

    def find_oldest_record(self, history_to_check=60):

        self.api.login()
        min = (datetime.today() - timedelta(days=history_to_check)).timestamp()
        max = datetime.today().timestamp()
        while min < max:
            mid = (min + max) // 2
            if self._check_date_valid(datetime.fromtimestamp(mid)):
                max = mid
            else:
                min = mid + 1
        return datetime.fromtimestamp(min)
        # while True:
        #     if max < min:
        #         return -1
        #     m = (min + max) // 2
        #     if seq[m] < t:
        #         min = m + 1
        #     elif seq[m] > t:
        #         max = m - 1
        #     else:
        #         return m

    def _check_date_valid(self, date):
        data = self.api.get_data(date)
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

        for data_item in filtered_data:
            db_rec = dict_to_record_objects(data_item)
            self.persistence.add_record(db_rec)
