import json
import ssl
from urllib.request import urlopen

from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import login_required, current_user

from app import csrf
from app.email import send_email
from app.models import TickerData, Candidate, UserSetting
from app.research.views import research_ticker

from flask_cors import CORS, cross_origin
import yfinance as yf

candidates = Blueprint('candidates', __name__)


@candidates.route('usercandidates', methods=['GET', 'POST'])
@login_required
def usercandidates():
    if not current_user.admin_confirmed or not current_user.signature:
        return redirect(url_for('station.download'))
    candidates = Candidate.query.filter_by(email=current_user.email).all()
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()
    admin_candidates = {}
    if user_settings.server_use_system_candidates:
        admin_candidates = Candidate.query.filter_by(email='support@algotrader.company', enabled=True).all()
    return render_template('candidates/usercandidates.html', admin_candidates=admin_candidates, candidates=candidates,
                           user=current_user, form=None)


@candidates.route('removecandidate/', methods=['POST'])
@csrf.exempt
def removecandidate():
    ticker = request.form['ticker_to_remove']
    candidate = Candidate.query.filter_by(email=current_user.email, ticker=ticker).first()
    candidate.delete_candidate()
    return redirect(url_for('candidates.usercandidates'))


@candidates.route('enabledisable/', methods=['POST'])
@csrf.exempt
def enabledisable():
    ticker = request.form['ticker_to_change']
    candidate = Candidate.query.filter_by(email=current_user.email, ticker=ticker).first()
    candidate.change_enabled_state()
    return redirect(url_for('candidates.usercandidates'))


@csrf.exempt
@candidates.route('/info', methods=['GET'])
def info():
    # # Test
    # user = User.query.filter_by(email='liliana.isr@gmail.com').first()
    # send_email(recipient='liliana.isr@gmail.com',
    #            user=user,
    #            subject='Algotrader: Black Swan is suspected!',
    #            template='account/email/black_swan')
    # # End Test

    ticker = request.args['ticker_to_show']
    candidate = Candidate.query.filter_by(ticker=ticker).first()
    m_data = TickerData.query.filter_by(ticker=ticker).order_by(TickerData.updated_server_time.desc()).first()
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()
    td_history = TickerData.query.filter_by(ticker=ticker).order_by(TickerData.updated_server_time.asc()).all()
    hist_dates = []
    hist_algo_ranks = []
    # hist_tr_ranks = []
    # hist_fmp_score = []
    # hist_yahoo_rank = []
    # stock_invest_rank = []
    for td in td_history:
        hist_dates.append(td.updated_server_time.strftime("%d %b, %Y"))
        hist_algo_ranks.append(td.algotrader_rank)
        # hist_tr_ranks.append(td.tipranks)
        # hist_fmp_score.append(td.fmp_score)
        # hist_yahoo_rank.append(td.yahoo_rank)
        # stock_invest_rank.append(td.stock_invest_rank)
    return render_template('candidates/ticker_info.html', user_settings=user_settings,
                           candidate=candidate,
                           market_data=m_data,
                           hist_dates=hist_dates,
                           hist_algo_ranks=hist_algo_ranks)
                           # hist_tr_ranks=hist_tr_ranks,
                           # hist_fmp_score=hist_fmp_score,
                           # hist_yahoo_rank=hist_yahoo_rank,
                           # stock_invest_rank=stock_invest_rank)


@csrf.exempt
@candidates.route('/get_info_ticker/<ticker>', methods=['GET'])
@cross_origin(origin='*',headers=['Content-Type', 'Authorization'])
def get_info_ticker(ticker):
    info = yf.Ticker(ticker).info
    return json.dumps(info)


def fill_ticker_data_from_yahoo(c):
    candidate_data = yf.Ticker(c.ticker).info
    if candidate_data is not None:
        c.company_name = candidate_data.longName
        c.full_description = candidate_data.longBusinessSummary
        c.exchange = candidate_data.exchange
        c.industry = candidate_data.industry
        c.sector = candidate_data.sector
        c.logo = candidate_data.logo_url
        c.update_candidate()
        research_ticker(c.ticker)
        return True
    return False


