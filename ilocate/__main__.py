from ilocate.save_to_log import *


def main():
    """Main routine of ilocate."""
    # history = get_data("2017-10-4")
    last_record = persistence.latest_record_datetime
    history2 = get_data_rg(datetime(2018, 11, 3), datetime.today())
    # print(history)

    for data in history2:
        db_rec = RECORD(speed=data['speed'],
                        dist_from_last=data['dist_from_last'],
                        device_state=data['state'],
                        lat=data['lat'], lon=data['lon'],
                        time_from_last=data['time_from_last'],
                        timestamp=data['timestamp'],
                        date=data['date'], time=data['time'],
                        dt=data['datetime'])
        persistence.add_record(db_rec)

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

