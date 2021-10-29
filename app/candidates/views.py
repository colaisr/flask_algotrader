from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import login_required, current_user

from app import csrf
from app.models import TickerData, Candidate, UserSetting
import app.enums as enum

candidates = Blueprint('candidates', __name__)


@candidates.route('usercandidates', methods=['GET', 'POST'])
@login_required
def usercandidates():
    # if not current_user.admin_confirmed or not current_user.signature:
    #     return redirect(url_for('station.download'))
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
    for td in td_history:
        hist_dates.append(td.updated_server_time.strftime("%d %b, %Y"))
        hist_algo_ranks.append(td.algotrader_rank)
    return render_template('candidates/ticker_info.html', user_settings=user_settings,
                           candidate=candidate,
                           market_data=m_data,
                           hist_dates=hist_dates,
                           hist_algo_ranks=hist_algo_ranks)






