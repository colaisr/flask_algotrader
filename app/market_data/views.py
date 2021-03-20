import json
import ssl
from urllib.request import urlopen

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for, jsonify,
)
from datetime import datetime, date, timedelta
from app import db, csrf
from app.models import User, Connection, Report, TickerData

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
    received_data=request_data["tickers"]
    logged_user = request_data["user"]
    parsed_data = json.loads(received_data)
    for marker in parsed_data:
        ticker=marker['ticker']
        yahoo_avdropP=marker['yahoo_avdropP']
        yahoo_avspreadP=marker['yahoo_avspreadP']
        tipranks=marker['tipranks']
        tiprank_updated=datetime.fromisoformat(marker['tiprank_updated'])
        fmp_pe = marker['fmp_pe']
        fmp_rating = marker['fmp_rating']
        fmp_score = marker['fmp_score']
        fmp_updated = datetime.fromisoformat(marker['fmp_updated'])
        t=TickerData(ticker=ticker,
                     yahoo_avdropP=yahoo_avdropP,
                     yahoo_avspreadP=yahoo_avspreadP,
                     tipranks=tipranks,
                     tiprank_updated=tiprank_updated,
                     fmp_pe=fmp_pe,
                     fmp_rating=fmp_rating,
                     fmp_score=fmp_score,
                     fmp_updated=fmp_updated,
                     updated_by_user=logged_user)
        if int(t.tipranks)!=0:
            t.update_ticker_data()

    return "Market data updated at server"
@csrf.exempt
@marketdata.route('/retrievemarketdata', methods=['GET'])
def retrievemarketdata():
    request_data = request.get_json()
    received_data=request_data["tickers"]
    logged_user = request_data["user"]
    parsed_data = json.loads(received_data)
    requested_tickers={}
    for t in parsed_data:
        td=TickerData.query.filter_by(ticker=t).first()
        if td is None:#not data-fake
            td=TickerData(ticker=t,
                          yahoo_avdropP=0,
                          yahoo_avspreadP=0,
                          tipranks=0,
                          tiprank_updated=(datetime.today() - timedelta(days=1)),
                          fmp_updated=(datetime.today() - timedelta(days=1)))

        tdj=json.dumps(td.toDictionary())
        requested_tickers[td.ticker]=tdj
    parsed_response=json.dumps(requested_tickers)
    return requested_tickers
