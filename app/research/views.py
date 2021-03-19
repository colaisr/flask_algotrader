

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
from app.models import User, Connection, Report, TickerData, Candidate
from app.research.fmp_research import get_fmp_pe_for_ticker, get_fmp_ratings_score_for_ticker
from app.research.tipranks_research import get_tiprank_for_ticker
from app.research.yahoo_research import get_yahoo_stats_for_ticker

research = Blueprint('research', __name__)



@csrf.exempt
@research.route('/updatemarketdataforcandidate', methods=['POST'])
def updatemarketdataforcandidate():
    ticker=request.form['ticker_to_update']
    marketdata = TickerData.query.filter_by(ticker=ticker).first()
    marketdata.tipranks=get_tiprank_for_ticker(ticker)
    marketdata.fmp_pe=get_fmp_pe_for_ticker(ticker)
    marketdata.fmp_rating,marketdata.fmp_score=get_fmp_ratings_score_for_ticker(ticker)
    marketdata.yahoo_avdropP, marketdata.yahoo_avspreadP = get_yahoo_stats_for_ticker(ticker)
    ct=datetime.now()
    marketdata.tiprank_updated=ct
    marketdata.fmp_updated=ct
    marketdata.update_ticker_data()

    return redirect(url_for('admin.market_data'))

