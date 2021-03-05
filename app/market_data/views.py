import json
import ssl
from urllib.request import urlopen

import fmpsdk
import jsonpickle
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
apikey='f6003a61d13c32709e458a1e6c7df0b0'

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def get_fmg_pe_rating_for_ticker(s):
    # data=fmpsdk.financial_ratios(apikey=apikey, symbol=s)
    url = ("https://financialmodelingprep.com/api/v3/ratios-ttm/"+s+"?apikey="+apikey)
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    parsed=json.loads(data)
    pe=parsed[0]['peRatioTTM']
    url = ("https://financialmodelingprep.com/api/v3/rating/"+s+"?apikey="+apikey)
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    parsed=json.loads(data)
    rating=parsed[0]['rating']
    score = parsed[0]['ratingScore']

    return pe,rating,score


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

@marketdata.route('updatefmpall/', methods=['POST'])
@csrf.exempt
def updatefmpall():
    td = TickerData.query.all()
    for candidate in td:
        pe, rating, score=get_fmg_pe_rating_for_ticker(candidate.ticker)
        candidate.fmp_pe=pe
        candidate.fmp_rating=rating
        candidate.fmp_score=score
        candidate.fmp_updated=datetime.today()
        db.session.commit()
        i=3
    return redirect(url_for('admin.market_data'))
