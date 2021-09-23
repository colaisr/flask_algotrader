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


def get_fmp_ticker_data(ticker):
    fmpkey = 'f6003a61d13c32709e458a1e6c7df0b0'
    url = ("https://financialmodelingprep.com/api/v3/profile/" + ticker + "?apikey=" + fmpkey)
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    parsed = json.loads(data)
    ticker_data = {}
    try:
        ticker_data['company_name'] = parsed[0]['companyName']
        ticker_data['full_description'] = parsed[0]['description']
        ticker_data['exchange'] = parsed[0]['exchangeShortName']
        ticker_data['industry'] = parsed[0]['industry']
        ticker_data['sector'] = parsed[0]['sector']
        ticker_data['logo'] = parsed[0]['image']
        ticker_data['isEtf'] = parsed[0]['isEtf']
    except:
        print('failed to extract fmp')
        ticker_data = None
    return ticker_data


@candidates.route('updatecandidate/', methods=['POST'])
@csrf.exempt
def updatecandidate():
    c = Candidate()
    c.ticker = request.form['txt_ticker']
    c.reason = request.form['txt_reason']
    c.email = current_user.email
    c.enabled = True
    candidate_data = get_fmp_ticker_data(c.ticker)
    if candidate_data is not None:
        c.company_name = candidate_data['company_name']
        c.full_description = candidate_data['full_description']
        c.exchange = candidate_data['exchange']
        c.industry = candidate_data['industry']
        c.sector = candidate_data['sector']
        c.logo = candidate_data['logo']

        c.update_candidate()
        research_ticker(c.ticker)

    return redirect(url_for('candidates.usercandidates'))


@candidates.route('add_by_spider', methods=['POST'])
@csrf.exempt
def add_by_spider():
    ticker_to_add = request.form['ticker_to_add']
    try:
        candidate = Candidate.query.filter_by(email='support@algotrader.company', ticker=ticker_to_add).first()
        if candidate is not None:
            print('adding ' + ticker_to_add)
            c = Candidate()
            c.ticker = ticker_to_add
            c.reason = "added automatically"
            c.email = 'support@algotrader.company'
            c.enabled = True
            candidate_data = get_fmp_ticker_data(c.ticker)
            if candidate_data is not None:
                if not candidate_data['isEtf']:
                    c.company_name = candidate_data['company_name']
                    c.full_description = candidate_data['full_description']
                    c.exchange = candidate_data['exchange']
                    c.industry = candidate_data['industry']
                    c.sector = candidate_data['sector']
                    c.logo = candidate_data['logo']

                    c.update_candidate()
                    r = research_ticker(c.ticker)
                    print('successfully added candidate')
                    return "successfully added candidate"
                else:
                    print(ticker_to_add + " skept - it is ETF- not supported...")
                    return "skept candidate"
            else:
                print(ticker_to_add + " skept no FMP data...")
                return "skept candidate"
        else:
            return "candidate exist"
    except:
        send_email(recipient='cola.isr@gmail.com',
                   subject='Algotrader adding candidate problem with ' + ticker_to_add,
                   template='account/email/research_issue',
                   ticker=ticker_to_add)
        print("failed to add candidate")
        return "exception in candidate " + ticker_to_add
    # else:
    #     print("skept-exist")
    #     return "skept"


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
