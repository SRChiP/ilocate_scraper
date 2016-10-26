import datetime


class DialogURLs(object):

    @staticmethod
    def login_url(usernumber, password):
        return {
            'url': "http://locate.dialog.lk/web/index.php",
            'data': {"LoginForm[username]": usernumber, "LoginForm[password]": password},
            'params': {"r": 'site/login'}
        }

    @staticmethod
    def current_url():
        return {
            'url': "http://locate.dialog.lk/web/index.php",
            'params': {"r": "/iLocateWeb/location/getCurrentData"}
        }

    @staticmethod
    def history_url(carnumber, date):
        if isinstance(date, str):
            date_str = date
        else:
            date = datetime.datetime.now()
            date_str = date.strftime('%Y-%m-%d')
        return {
            'url': "http://locate.dialog.lk/web/index.php",
            'data': {"number": carnumber, "start_time": "12:00:00 AM", "end_time": "11:59:59 PM", "date": date_str},
            'params': {"r": "/iLocateWeb/location/getHistoryData"}
        }
