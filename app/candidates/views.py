from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import login_required, current_user

from app import csrf, db
from app.models import TickerData, Candidate, UserSetting, Fgi_score
from sqlalchemy import text

candidates = Blueprint('candidates', __name__)


@candidates.route('today', methods=['GET', 'POST'])
@login_required
def today():
    # if not current_user.admin_confirmed or not current_user.signature:
    #     return redirect(url_for('station.download'))
    query_text = "select a.* from Tickersdata a join (  select Tickersdata.`ticker`, max(Tickersdata.`updated_server_time`) as updated_server_time  from Tickersdata group by Tickersdata.`ticker`) b on b.`ticker`=a.`ticker` and b.`updated_server_time`=a.`updated_server_time`"
    marketdata = db.session.query(TickerData).from_statement(text(query_text)).all()
    # marketdata_dic = marketdata.toDictionary()
    algo_rank = {m.ticker: m.algotrader_rank for m in marketdata}
    candidates = Candidate.query.filter_by(email=current_user.email).all()
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()
    user_fgi = user_settings.algo_min_emotion

    market_emotion = Fgi_score.query.order_by(Fgi_score.score_time.desc()).first()
    if market_emotion.fgi_value < user_settings.algo_min_emotion:
        fgi_text_color = 'danger'
    else:
        fgi_text_color = 'success'

    admin_candidates = {}
    if user_settings.server_use_system_candidates:
        admin_candidates = Candidate.query.filter_by(email='support@algotrader.company', enabled=True).all()
    return render_template('candidates/today.html', admin_candidates=admin_candidates, candidates=candidates,
                           user=current_user, market_emotion=market_emotion, user_fgi=user_fgi, fgi_text_color=fgi_text_color, algo_rank=algo_rank,  form=None)


@candidates.route('usercandidates', methods=['GET', 'POST'])
@login_required
def usercandidates():
    # if not current_user.admin_confirmed or not current_user.signature:
    #     return redirect(url_for('station.download'))
    query_text = "select a.* from Tickersdata a join (  select Tickersdata.`ticker`, max(Tickersdata.`updated_server_time`) as updated_server_time  from Tickersdata group by Tickersdata.`ticker`) b on b.`ticker`=a.`ticker` and b.`updated_server_time`=a.`updated_server_time`"
    marketdata = db.session.query(TickerData).from_statement(text(query_text)).all()
    # marketdata_dic = marketdata.toDictionary()
    algo_rank = {m.ticker: m.algotrader_rank for m in marketdata}
    candidates = Candidate.query.filter_by(email=current_user.email).all()
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()

    market_emotion = Fgi_score.query.order_by(Fgi_score.score_time.desc()).first()
    if market_emotion.fgi_value < user_settings.algo_min_emotion:
        fgi_text_color = 'danger'
    else:
        fgi_text_color = 'success'

    admin_candidates = {}
    if user_settings.server_use_system_candidates:
        admin_candidates = Candidate.query.filter_by(email='support@algotrader.company', enabled=True).all()
    return render_template('candidates/usercandidates.html', admin_candidates=admin_candidates, candidates=candidates,
                           user=current_user, market_emotion=market_emotion, fgi_text_color=fgi_text_color, algo_rank=algo_rank,  form=None)


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






