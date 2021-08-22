import json
import math

from flask import (
    Blueprint,
    redirect,
    request,
    url_for
)
from datetime import datetime
from app import csrf
from app.email import send_email
from app.models import TickerData, Candidate, LastUpdateSpyderData
from app.research.fmp_research import get_fmp_ratings_score_for_ticker
from app.research.stock_invest_research import get_stock_invest_rank_for_ticker
from app.research.tipranks_research import get_tiprank_for_ticker
from app.research.yahoo_finance_research import get_yahoo_rank_for_ticker
from app.research.yahoo_research import get_yahoo_stats_for_ticker

research = Blueprint('research', __name__)


@csrf.exempt
@research.route('/updatemarketdataforcandidate', methods=['POST'])
def updatemarketdataforcandidate():
    ticker = request.form['ticker_to_update']
    try:
        research_ticker(ticker)
    except:
        print('problem with research')
    return redirect(url_for('admin.market_data'))


@csrf.exempt
@research.route('/savelasttimeforupdatedata', methods=['POST'])
def savelasttimeforupdatedata():
    error_status = request.form['error_status']
    error_message = request.form['error_message']
    now = datetime.utcnow()
    try:
        last_update_data = LastUpdateSpyderData.query.first()
        if last_update_data is None:
            last_update_data = LastUpdateSpyderData()
        last_update_data.process_date_time = now
        if error_status == '1':
            last_update_data.error_status = True
            last_update_data.error_message = error_message
        else:
            last_update_data.last_update_date = now
            last_update_data.error_status = False
        last_update_data.update_data()
    except:
        print('problem with update last date')
    return redirect(url_for('admin.market_data'))


def research_ticker(ticker):
    marketdata = TickerData()
    marketdata.ticker = ticker
    try:
        marketdata.tipranks, marketdata.twelve_month_momentum = get_tiprank_for_ticker(ticker)
    except:
        send_email(recipient='cola.isr@gmail.com',
                   subject='Algotrader research Tipranks problem with ' + ticker,
                   template='account/email/research_issue',
                   ticker=ticker)
    try:
        marketdata.stock_invest_rank = get_stock_invest_rank_for_ticker(ticker)
    except:
        send_email(recipient='cola.isr@gmail.com',
                   subject='Algotrader research Stock Invest problem with ' + ticker,
                   template='account/email/research_issue',
                   ticker=ticker)
    try:
        marketdata.yahoo_rank, marketdata.under_priced_pnt = get_yahoo_rank_for_ticker(ticker)
    except:
        print('exception occured for ' + ticker)
    marketdata.fmp_rating, marketdata.fmp_score = get_fmp_ratings_score_for_ticker(ticker)
    marketdata.yahoo_avdropP, marketdata.yahoo_avspreadP = get_yahoo_stats_for_ticker(ticker)
    if math.isnan(marketdata.yahoo_avdropP):
        marketdata.yahoo_avdropP = 0
    if math.isnan(marketdata.yahoo_avspreadP):
        marketdata.yahoo_avspreadP = 0
    ct = datetime.utcnow()

    marketdata.updated_server_time = ct
    marketdata.add_ticker_data()


@csrf.exempt
@research.route('/alltickers', methods=['GET'])  # for use from the task
def alltickers():
    cands = Candidate.query.filter_by(enabled=True).group_by(Candidate.ticker).all()
    resp = []
    for c in cands:
        resp.append(c.ticker)
    return json.dumps(resp)
