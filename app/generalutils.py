import json
import ssl
import certifi
import urllib
from dateutil import tz
from pytz import timezone
from sqlalchemy.ext.declarative import DeclarativeMeta
from datetime import datetime, date
from urllib.request import urlopen


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


def check_for_blanks(str):
    # myString is not None AND myString is not empty or blank
    if str and str.strip():
        return False
    # myString is None OR myString is empty or blank
    return True


def is_market_open():
    url = ('https://financialmodelingprep.com/api/v3/is-the-market-open?apikey=f6003a61d13c32709e458a1e6c7df0b0')
    state = 'Error'
    try:
        context = ssl._create_unverified_context()
        response = urlopen(url, context=context)
        data = response.read().decode("utf-8")
        parsed = json.loads(data)
        state = parsed['isTheStockMarketOpen']
        if state:
            state = "Open"
        else:
            state = "Closed"
    except:
        pass
    return state


def api_request_get(url):
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    return response.read().decode("utf-8")


def api_request_post(url, request_data):
    data = urllib.parse.urlencode(request_data)
    data = data.encode('ascii')
    context = ssl.create_default_context(cafile=certifi.where())
    response = urllib.request.urlopen(url, data, context=context)
    return response.read()


class JsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj.__class__, DeclarativeMeta):
            # an SQLAlchemy class
            fields = {}
            for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                data = obj.__getattribute__(field)
                if isinstance(data, (datetime, date)):
                    data = datetime.isoformat(data)
                try:
                    json.dumps(data)  # this will fail on non-encodable values, like other classes
                    fields[field] = data
                except TypeError:
                    fields[field] = None
            # a json-encodable dict
            return fields
        return json.JSONEncoder.default(self, obj)


