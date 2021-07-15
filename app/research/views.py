import json

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for, jsonify,
)
from datetime import datetime, date, timedelta

from flask_login import current_user

from app import db, csrf
from app.email import send_email
from app.models import User, Connection, Report, TickerData, Candidate
from app.research.fmp_research import get_fmp_pe_for_ticker, get_fmp_ratings_score_for_ticker
from app.research.tipranks_research import get_tiprank_for_ticker
from app.research.yahoo_research import get_yahoo_stats_for_ticker

research = Blueprint('research', __name__)


@csrf.exempt
@research.route('/updatemarketdataforcandidate', methods=['POST'])
def updatemarketdataforcandidate():
    ticker = request.form['ticker_to_update']
    try:
        research_ticker(ticker)
    except:
        send_email(recipient='cola.isr@gmail.com',
                   subject='Algotrader research problem with '+ticker,
                   template='account/email/research_issue',
                   ticker=ticker)

    return redirect(url_for('admin.market_data'))


def research_ticker(ticker):
    #todo exception handling
    marketdata = TickerData()
    marketdata.ticker=ticker
    marketdata.tipranks = get_tiprank_for_ticker(ticker)
    marketdata.fmp_pe = get_fmp_pe_for_ticker(ticker)
    marketdata.fmp_rating, marketdata.fmp_score = get_fmp_ratings_score_for_ticker(ticker)
    marketdata.yahoo_avdropP, marketdata.yahoo_avspreadP = get_yahoo_stats_for_ticker(ticker)
    ct = datetime.now()

    marketdata.updated_server_time = ct
    marketdata.add_ticker_data()


@csrf.exempt
@research.route('/alltickers', methods=['GET'])  # for use from the task
def alltickers():
    # marketdata = TickerData.query.group_by(TickerData.ticker).all()
    cands=Candidate.query.filter_by(enabled=True).group_by(Candidate.ticker).all()
    resp = []
    for c in cands:
        resp.append(c.ticker)

    return json.dumps(resp)
