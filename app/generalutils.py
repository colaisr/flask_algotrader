from dateutil import tz
from datetime import datetime
from pytz import timezone


def utc_datetime_to_local(utc):
    from_zone = tz.tzutc()
    to_zone = tz.tzlocal()

    # Tell the datetime object that it's in UTC time zone since
    # datetime objects are 'naive' by default
    utc = utc.replace(tzinfo=from_zone)

    # Convert time zone
    central = utc.astimezone(to_zone)
    return central


def local_datetime_to_utc(local):
    to_zone = tz.tzutc()
    from_zone = tz.tzlocal()
    local = local.replace(tzinfo=from_zone)
    utc = local.astimezone(to_zone)
    return utc


def get_by_timezone(tz_str):
    tz = timezone(tz_str)
    date = datetime.now(tz)
    return date

def user_online_status(report_time, station_interval_worker_sec):
    current = datetime.utcnow()
    delta = (current - report_time).seconds
    refresh_rate = station_interval_worker_sec * 2  # takes time to process
    if delta < refresh_rate:
        online = True
    else:
        online = False
    return online


