from datetime import datetime


def get_event_datetime_string(event):
    try:
        event_datetime = datetime.strptime(event.key, '%Y-%m-%dT%H:%M:%S%z')
    except ValueError:
        event_datetime = datetime.strptime("{}T20:00:00-0400".format(event.key), '%Y-%m-%dT%H:%M:%S%z')
    return datetime.strftime(event_datetime, '%Y-%m-%d %H:%M:%S')