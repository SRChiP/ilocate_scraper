from json import JSONDecodeError

import requests
import functools

from urls import DialogURLs

import time
import math


# Retry decorator with exponential backoff


def retry(tries=1, delay=2, backoff=2):
    '''Retries a function or method until it returns True.

  delay sets the initial delay in seconds, and backoff sets the factor by which
  the delay should lengthen after each failure. backoff must be greater than 1,
  or else it isn't really a backoff. tries must be at least 0, and delay
  greater than 0.'''
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
    def get_data(self, date, carnumber=None):
        carnumber = self.carnumber if not carnumber else carnumber
        response = self.http_session.post(**DialogURLs.history_url(carnumber, date))
        json_data = response.json()
        if not json_data['success']:
            raise LookupError(json_data['error'])
        return json_data['data']
