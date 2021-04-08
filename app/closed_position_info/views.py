import json
import ssl
from urllib.request import urlopen
from datetime import datetime

import numpy as np
import pandas
import yfinance as yf

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
from app.models import User, Connection, Report, TickerData, Position

closed_position_info = Blueprint('closed_position_info', __name__)
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
@closed_position_info.route('/view', methods=['GET'])
def view():
    id=request.args['position_to_show']
    position = Position.query.filter_by(id=id).first()
    hist=TickerData.query.filter_by(ticker=position.ticker).order_by(TickerData.updated_server_time.asc()).all()
    rank_array=[]
    for h in hist:
        rank_array.append([str(h.updated_server_time.strftime("%Y-%m-%d %H:%M:%S")),h.tipranks])
    return render_template('userview/closed_position_info.html',position=position,rank_array=rank_array)


# def get_stock_rank(s):
#     pass
#     df=yf.download(s,interval = "1m", period = "1y")
#
#     s=df["Close"]
#     list_of_dates=s.index.to_list()
#     conv=[]
#     for d in list_of_dates:
#         ts=datetime.timestamp(d)
#         conv.append([ts,s[d]])
#         dt_object = datetime.fromtimestamp(ts)
#         i=3
#     return conv
