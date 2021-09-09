import json

from flask import (
    Blueprint,
    request
)
from datetime import datetime, date
from app import csrf
from app.models import TickerData

marketdata = Blueprint('marketdata', __name__)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


@csrf.exempt
@marketdata.route('/updatemarketdata', methods=['POST'])
def updatemarketdata():
    request_data = request.get_json()
    received_data = request_data["tickers"]
    parsed_data = json.loads(received_data)
    for marker in parsed_data:
        ticker = marker['ticker']
        yahoo_avdropP = marker['yahoo_avdropP']
        yahoo_avspreadP = marker['yahoo_avspreadP']
        tipranks = marker['tipranks']
        fmp_pe = marker['fmp_pe']
        fmp_rating = marker['fmp_rating']
        fmp_score = marker['fmp_score']
        t = TickerData(ticker=ticker,
                       yahoo_avdropP=yahoo_avdropP,
                       yahoo_avspreadP=yahoo_avspreadP,
                       tipranks=tipranks,
                       fmp_pe=fmp_pe,
                       fmp_rating=fmp_rating,
                       fmp_score=fmp_score)
        if int(t.tipranks) != 0:
            t.add_ticker_data()

    return "Market data updated at server"


@csrf.exempt
@marketdata.route('/retrievemarketdata', methods=['GET'])
def retrievemarketdata():
    request_data = request.get_json()
    received_data = request_data["tickers"]
    parsed_data = json.loads(received_data)
    requested_tickers = {}
    for t in parsed_data:
        td = TickerData.query.filter_by(ticker=t).order_by(TickerData.updated_server_time.desc()).first()
        if td is None:  # not data-fake
            td = TickerData(ticker=t,
                            yahoo_avdropP=0,
                            yahoo_avspreadP=0,
                            tipranks=0)

        tdj = json.dumps(td.toDictionary())
        requested_tickers[td.ticker] = tdj
    return requested_tickers

