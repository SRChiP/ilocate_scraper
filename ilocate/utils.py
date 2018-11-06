import functools
import time

import math


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
            ex = None
            while mtries > 0:
                try:
                    rv = f(*args, **kwargs)
                except Exception as e:
                    ex = e
                    mtries -= 1  # consume an attempt
                    time.sleep(mdelay)  # wait...
                    mdelay *= backoff  # make future wait longer
                    args[0].login()
                else:
                    return rv
            raise ex

        return f_retry  # true decorator -> decorated function

    return deco_retry  # @retry(arg[, ...]) -> true decorator
