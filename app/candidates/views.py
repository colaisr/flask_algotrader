import app.generalutils as general
import json
from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    url_for
)

from flask_login import login_required, current_user

from app import csrf, db
from datetime import datetime
from app.models import TickerData, Candidate, UserSetting, Fgi_score, LastUpdateSpyderData
from sqlalchemy import text


candidates = Blueprint('candidates', __name__)


@candidates.route('today', methods=['GET', 'POST'])
@login_required
def today():
    # test = "SELECT a.`algotrader_rank`, c.* FROM Candidates c left join Tickersdata a ON a.`ticker`=c.`ticker` JOIN (select Tickersdata.`ticker`, max(Tickersdata.`updated_server_time`) as updated_server_time from Tickersdata group by Tickersdata.`ticker`) b ON a.`ticker`=b.`ticker` AND a.`updated_server_time`=b.`updated_server_time` ORDER BY a.`algotrader_rank` desc"
    # test_res = db.engine.execute(text(test))

    last_update = db.session.query(LastUpdateSpyderData).order_by(
        LastUpdateSpyderData.start_process_time.desc()).first()
    bg_upd_color = "badge-success" if datetime.now().date() == last_update.last_update_date.date() and not last_update.error_status else "badge-danger"
    current_est_time = general.get_by_timezone('US/Eastern').time().strftime("%H:%M")
    trading_session_state = general.is_market_open()
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()
    user_fgi = user_settings.algo_min_emotion

    market_emotion = Fgi_score.query.order_by(Fgi_score.score_time.desc()).first()
    if market_emotion.fgi_value < user_settings.algo_min_emotion:
        fgi_text_color = 'danger'
    else:
        fgi_text_color = 'success'

    admin_email = 'support@algotrader.company'
    query = f"SELECT DISTINCT c.ticker, " \
            f"c.company_name, " \
            f"t.algotrader_rank AS last_rank, " \
            f"(t.algotrader_rank - pre.algotrader_rank) AS change_val, " \
            f"c.logo " \
            f"FROM Candidates c " \
            f"JOIN Tickersdata t ON t.ticker=c.ticker " \
            f"JOIN Tickersdata pre ON pre.ticker=t.ticker " \
            f"WHERE c.email = '{admin_email}' " \
            f"AND DATE(t.updated_server_time) >= subdate(DATE(NOW()), 1) " \
            f"AND DATE(pre.updated_server_time) >= subdate(DATE(NOW()), 2) " \
            f"AND DATE(t.updated_server_time) <> DATE(pre.updated_server_time) " \
            f"AND t.algotrader_rank >pre.algotrader_rank " \
            f"ORDER BY t.algotrader_rank desc"
    today_improovers_res = db.engine.execute(text(query))
    today_improovers = [dict(r.items()) for r in today_improovers_res]

    user_query = f"SELECT c.ticker, c.company_name, c.logo, c.sector, a.under_priced_pnt, case when a.algotrader_rank IS NULL then 0 ELSE a.algotrader_rank END AS algotrader_rank, a.twelve_month_momentum, a.beta, a.max_intraday_drop_percent FROM Candidates c JOIN Tickersdata a ON a.ticker=c.ticker JOIN (select Tickersdata.ticker, max(Tickersdata.updated_server_time) as updated_server_time from Tickersdata group by Tickersdata.ticker) b on b.ticker=a.ticker and b.updated_server_time=a.updated_server_time WHERE c.email='{current_user.email}'"
    candidates_res = db.engine.execute(text(user_query))
    candidates = [dict(r.items()) for r in candidates_res]

    # query_text = "select a.* from Tickersdata a join (  select Tickersdata.`ticker`, max(Tickersdata.`updated_server_time`) as updated_server_time  from Tickersdata group by Tickersdata.`ticker`) b on b.`ticker`=a.`ticker` and b.`updated_server_time`=a.`updated_server_time`"
    # marketdata = db.session.query(TickerData).from_statement(text(query_text)).all()
    # market_data = {m.ticker: m for m in marketdata}

    admin_query = "SELECT c.ticker, c.company_name, c.logo, c.sector, a.under_priced_pnt, case when a.algotrader_rank IS NULL then 0 ELSE a.algotrader_rank END AS algotrader_rank, a.twelve_month_momentum, a.beta, a.max_intraday_drop_percent FROM (SELECT * FROM Candidates WHERE enabled=1 GROUP BY ticker) c JOIN Tickersdata a ON a.ticker=c.ticker JOIN (select Tickersdata.ticker, max(Tickersdata.`updated_server_time`) as updated_server_time from Tickersdata group by Tickersdata.ticker ) b on b.ticker=a.ticker and b.updated_server_time=a.updated_server_time"
    admin_candidates_res = db.engine.execute(text(admin_query))
    admin_candidates = [dict(r.items()) for r in admin_candidates_res]

    signals_query = f"SELECT s.*,c.company_name, c.logo FROM TelegramSignals s JOIN Candidates c ON c.ticker=s.ticker WHERE DATE(s.received) = DATE(NOW())"
    signals_res = db.engine.execute(text(signals_query))
    signals = [dict(r.items()) for r in signals_res]

    return render_template('candidates/today.html',
                           user=current_user,
                           today_improovers=today_improovers,
                           market_emotion=market_emotion,
                           user_fgi=user_fgi,
                           fgi_text_color=fgi_text_color,
                           # market_data=market_data,
                           current_est_time=current_est_time,
                           trading_session_state=trading_session_state,
                           last_update_date=last_update.last_update_date.strftime("%d %b %H:%M"),
                           bg_upd_color=bg_upd_color,
                           admin_candidates=admin_candidates,
                           candidates=candidates,
                           candidates_json=json.dumps(candidates, cls=general.JsonEncoder),
                           # market_data_json=json.dumps(market_data, cls=general.JsonEncoder),
                           signals=signals,
                           form=None)


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


@candidates.route('/removecandidate_ajax', methods=['POST'])
@csrf.exempt
def removecandidate_ajax():
    ticker = request.form['ticker']
    candidate = Candidate.query.filter_by(email=current_user.email, ticker=ticker).first()
    candidate.delete_candidate()
    return json.dumps({'result': True})


@candidates.route('/enabledisable_ajax', methods=['POST'])
@csrf.exempt
def enabledisable_ajax():
    ticker = request.form['ticker']
    candidate = Candidate.query.filter_by(email=current_user.email, ticker=ticker).first()
    candidate.change_enabled_state()
    return json.dumps({'result': True})


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






