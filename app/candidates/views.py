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

    admin_query = "SELECT c.ticker, " \
                  "c.company_name, " \
                  "c.logo, c.sector, " \
                  "a.under_priced_pnt, " \
                  "case when a.algotrader_rank IS NULL then 0 ELSE a.algotrader_rank END AS algotrader_rank, " \
                  "a.twelve_month_momentum, " \
                  "a.beta, " \
                  "a.max_intraday_drop_percent " \
                  "FROM (SELECT * FROM Candidates " \
                  "WHERE enabled=1 GROUP BY ticker) c " \
                  "JOIN Tickersdata a ON a.ticker=c.ticker " \
                  "JOIN (select Tickersdata.ticker, " \
                  "max(Tickersdata.`updated_server_time`) as updated_server_time " \
                  "from Tickersdata group by Tickersdata.ticker ) b on b.ticker=a.ticker " \
                  "and b.updated_server_time=a.updated_server_time"

    admin_candidates_res = db.engine.execute(text(admin_query))
    admin_candidates = [dict(r.items()) for r in admin_candidates_res]

    return render_template('candidates/today.html',
                           user=current_user,
                           market_emotion=market_emotion,
                           user_fgi=user_fgi,
                           fgi_text_color=fgi_text_color,
                           current_est_time=current_est_time,
                           trading_session_state=trading_session_state,
                           last_update_date=last_update.last_update_date.strftime("%d %b %H:%M"),
                           bg_upd_color=bg_upd_color,
                           admin_candidates=admin_candidates,
                           form=None)


@candidates.route('/telegram_signals', methods=['GET'])
@csrf.exempt
def telegram_signals():
    signals_query = f"SELECT s.ticker, " \
                    f"s.signal_price, " \
                    f"s.target_price, " \
                    f"s.profit_percent, " \
                    f"s.days_to_get, " \
                    f"c.company_name, " \
                    f"c.logo " \
                    f"FROM TelegramSignals s " \
                    f"JOIN Candidates c ON c.ticker=s.ticker " \
                    f"WHERE DATE(s.received) = DATE(NOW())"
    signals_res = db.engine.execute(text(signals_query))
    signals = [dict(r.items()) for r in signals_res]
    return json.dumps(signals, cls=general.JsonEncoder)


@candidates.route('/today_improovers', methods=['GET'])
@csrf.exempt
def today_improovers():
    query = f"SELECT DISTINCT c.ticker, " \
            f"c.company_name, " \
            f"lst.algotrader_rank as last_rank, " \
            f"(lst.algotrader_rank - pre.algotrader_rank) AS change_val, " \
            f"c.logo FROM Candidates c " \
            f"join (SELECT a.ticker, " \
            f"MAX(a.updated_server_time) AS pre_server_time, " \
            f"b.last_updated_server_time " \
            f"from Tickersdata a " \
            f"JOIN (select Tickersdata.ticker, " \
            f"max(Tickersdata.updated_server_time) as last_updated_server_time " \
            f"from Tickersdata " \
            f"group by Tickersdata.ticker" \
            f") b on b.ticker=a.ticker and date(b.last_updated_server_time) > date(a.updated_server_time) " \
            f"group by a.ticker) d ON d.ticker=c.ticker " \
            f"JOIN Tickersdata lst ON lst.ticker=d.ticker " \
            f"AND lst.updated_server_time=d.last_updated_server_time " \
            f"JOIN Tickersdata pre ON pre.ticker=d.ticker " \
            f"AND pre.updated_server_time=d.pre_server_time  " \
            f"AND lst.algotrader_rank > pre.algotrader_rank " \
            f"ORDER BY lst.algotrader_rank desc"
    today_improovers_res = db.engine.execute(text(query))
    today_improovers = [dict(r.items()) for r in today_improovers_res]
    return json.dumps(today_improovers, cls=general.JsonEncoder)


@candidates.route('/user_candidates', methods=['GET'])
@csrf.exempt
def user_candidates():
    candidates = get_user_candidates()
    return json.dumps(candidates, cls=general.JsonEncoder)


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


@candidates.route('/removecandidate', methods=['POST'])
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
    candidates = get_user_candidates()
    return json.dumps(candidates, cls=general.JsonEncoder)


@candidates.route('/enabledisable_ajax', methods=['POST'])
@csrf.exempt
def enabledisable_ajax():
    result = {"color_status": "success", "message": "Ticker updated"}
    try:
        ticker = request.form['ticker']
        candidate = Candidate.query.filter_by(email=current_user.email, ticker=ticker).first()
        candidate.change_enabled_state()
    except Exception as e:
        result = {"color_status": "danger", "message": "Error in server"}
    return json.dumps(result)


@candidates.route('enabledisable/', methods=['POST'])
@csrf.exempt
def enabledisable():
    ticker = request.form['ticker_to_change']
    candidate = Candidate.query.filter_by(email=current_user.email, ticker=ticker).first()
    candidate.change_enabled_state()
    return redirect(url_for('candidates.usercandidates'))


@csrf.exempt
@candidates.route('/info/<ticker>', methods=['GET'])
def info(ticker):
    # # Test
    # user = User.query.filter_by(email='liliana.isr@gmail.com').first()
    # send_email(recipient='liliana.isr@gmail.com',
    #            user=user,
    #            subject='Algotrader: Black Swan is suspected!',
    #            template='account/email/black_swan')
    # # End Test

    # ticker = request.args['ticker_to_show']
    candidate = Candidate.query.filter_by(ticker=ticker).first()
    m_data = TickerData.query.filter_by(ticker=ticker).order_by(TickerData.updated_server_time.desc()).first()
    last_update = m_data.updated_server_time.date()
    bg_upd_color = "badge-success" if datetime.now().date() == last_update else "badge-warning"
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()
    score_bg = "bg-warning" if m_data.algotrader_rank < user_settings.algo_min_rank else "bg-success"
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
                           hist_algo_ranks=hist_algo_ranks,
                           last_update=last_update,
                           bg_upd_color=bg_upd_color,
                           score_bg=score_bg)


def get_user_candidates():
    user_query = f"SELECT c.ticker, " \
                 f"c.company_name, " \
                 f"c.logo, " \
                 f"c.sector, " \
                 f"c.reason, " \
                 f"c.enabled," \
                 f"a.under_priced_pnt, " \
                 f"case when a.algotrader_rank IS NULL then 0 ELSE a.algotrader_rank END AS algotrader_rank, " \
                 f"a.twelve_month_momentum, " \
                 f"a.beta, " \
                 f"a.max_intraday_drop_percent " \
                 f"FROM Candidates c " \
                 f"JOIN Tickersdata a ON a.ticker=c.ticker " \
                 f"JOIN (select Tickersdata.ticker, " \
                 f"max(Tickersdata.updated_server_time) as updated_server_time " \
                 f"from Tickersdata group by Tickersdata.ticker" \
                 f") b on b.ticker=a.ticker and b.updated_server_time=a.updated_server_time " \
                 f"WHERE c.email='{current_user.email}'" \
                 f"order by algotrader_rank desc"
    candidates_res = db.engine.execute(text(user_query))
    candidates = [dict(r.items()) for r in candidates_res]
    return candidates






