class DialogURLs(object):

    @staticmethod
    def login_url(usernumber, password) -> dict:
        return {
            'url': "http://locate.dialog.lk/web/index.php",
            'data': {"LoginForm[username]": usernumber, "LoginForm[password]": password},
            'params': {"r": 'site/login'}
        }

    @staticmethod
    def current_url() -> dict:
        return {
            'url': "http://locate.dialog.lk/web/index.php",
            'params': {"r": "/iLocateWeb/location/getCurrentData"}
        }

    @staticmethod
    def history_url(carnumber, check_date, start_time, end_time) -> dict:
        return {
            'url': "http://locate.dialog.lk/web/index.php",
            'data': {"number": carnumber, "start_time": start_time, "end_time": end_time, "date": check_date},
            'params': {"r": "/iLocateWeb/location/getHistoryData"}
        }
