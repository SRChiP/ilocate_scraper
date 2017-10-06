import datetime
from json import JSONDecodeError

import requests
import functools

from urls import DialogURLs

import time
import math


# Retry decorator with exponential backoff
def retry(tries=1, delay=2, backoff=2):
    """
    Retries a function or method until it gives out no exceptions.

    :param tries: Number of times to try reexecuting the code before it fails.
    :param delay: delay sets the initial delay in seconds, and backoff sets the factor by which
        the delay should lengthen after each failure.
    :param backoff: backoff must be greater than 1, or else it isn't really a backoff.
    :return:
    """
    if backoff <= 1:
        raise ValueError("backoff must be greater than 1")
    tries = math.floor(tries)
    if tries < 0:
        raise ValueError("tries must be 0 or greater")
    if delay <= 0:
        raise ValueError("delay must be greater than 0")

    def deco_retry(f):
        @functools.wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay  # make mutable

            while mtries > 0:
                try:
                    rv = f(*args, **kwargs)
                except Exception as e:
                    mtries -= 1  # consume an attempt
                    time.sleep(mdelay)  # wait...
                    mdelay *= backoff  # make future wait longer
                    args[0].login()
                else:
                    return rv
            raise

        return f_retry  # true decorator -> decorated function

    return deco_retry  # @retry(arg[, ...]) -> true decorator


class IlocateAPI(object):
    def __init__(self, usernumber, password, carnumber=None):
        self.usernumber = usernumber
        self.password = password
        self.carnumber = None
        self.http_session = requests.session()

    def login(self, automatically_set_carnumber=True):
        login_response = self.http_session.post(**DialogURLs.login_url(self.usernumber, self.password))
        if login_response.status_code != 200 or 'maps.googleapis.com' not in login_response.text:
            raise LookupError('Could not login into the portal.')
        if automatically_set_carnumber:
            recent_data = self.get_recent_data()
            if len(recent_data) == 1:
                self.carnumber = recent_data[0]['number']

    @retry()
    def get_recent_data(self):
        current_data = self.http_session.post(**DialogURLs.current_url()).json()
        if not current_data['success']:
            raise LookupError(current_data['error'])
        return current_data['data']

    @retry()
    def get_data(self, date, start_time=datetime.time(0, 0, 0), carnumber=None) -> dict:
        if isinstance(date, datetime.datetime):
            date = date.date()
            date_str = "{:%Y-%m-%d}".format(date)
        elif isinstance(date, datetime.date):
            date_str = "{:%Y-%m-%d}".format(date)
        elif isinstance(date, str):
            date_str = date
        if isinstance(start_time, datetime.time):
            start_time_str = "{:%I:%M:%S %p}".format(start_time)
        else:
            start_time_str = start_time

        carnumber = self.carnumber if not carnumber else carnumber
        response = self.http_session.post(**DialogURLs.history_url(carnumber, date, start_time_str, "11:59:59 PM"))
        json_data = response.json()
        if not json_data['success']:
            raise LookupError(json_data['error'])
        return json_data['data']

    @retry()
    def get_data_range(self, start_date: datetime.datetime, end_date: datetime.datetime, carnumber=None) -> list:
        if start_date > end_date:
            raise ValueError("start_date is after end_date.")
        st_day = start_date.date()
        ed_day = end_date.date()
        number_of_days = (ed_day - st_day).days
        carnumber = self.carnumber if not carnumber else carnumber

        response_list = []
        for iter_day in range(number_of_days + 1):
            current_day = st_day + datetime.timedelta(days=iter_day)
            start_time = "12:00:00 AM"
            end_time = "11:59:59 PM"
            if current_day == st_day:
                # If this is the start date
                start_time = start_date.strftime('%I:%M:%S %p')
            if current_day == ed_day:
                # If this is the ending day
                end_time = end_date.strftime('%I:%M:%S %p')
            date_string = current_day.strftime('%Y-%m-%d')

            response = self.http_session.post(**DialogURLs.history_url(carnumber, date_string, start_time, end_time))
            response_list.append(response)

        data_list = []
        for resp in response_list:
            json_data = resp.json()
            if not json_data['success']:
                raise LookupError(json_data['error'])
            data_list.extend(json_data['data'])

        return data_list
