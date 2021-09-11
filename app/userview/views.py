import json
import ssl
import app.generalutils as general
from datetime import datetime
from urllib.request import urlopen
from functools import reduce
from dateutil.relativedelta import relativedelta

from flask import (
    Blueprint,
    redirect,
    render_template,
    url_for,
    request
)
from flask_login import (
    current_user,
    login_required
)
from app.models import Position, Report, ReportStatistic, Candidate, UserSetting, LastUpdateSpyderData
from sqlalchemy import or_
from app import db

userview = Blueprint('userview', __name__)


def is_market_open():
    url = ('https://financialmodelingprep.com/api/v3/is-the-market-open?apikey=f6003a61d13c32709e458a1e6c7df0b0')
    state = 'Error'
    try:
        context = ssl._create_unverified_context()
        response = urlopen(url, context=context)
        data = response.read().decode("utf-8")
        parsed = json.loads(data)
        state = parsed['isTheStockMarketOpen']
        if state:
            state = "Open"
        else:
            state = "Closed"
    except:
        pass
    return state


@userview.route('traderstationstate', methods=['GET', 'POST'])
@login_required
def traderstationstate():
    if not current_user.admin_confirmed or not current_user.signature:
        return redirect(url_for('station.download'))

    report = Report.query.filter_by(email=current_user.email).first()
    settings = UserSetting.query.filter_by(email=current_user.email).first()

    last_update = db.session.query(LastUpdateSpyderData).order_by(LastUpdateSpyderData.start_process_time.desc()).first()
    bg_upd_color = "badge-success" if datetime.now().date() == last_update.last_update_date.date() and not last_update.error_status else "badge-danger"
    use_margin = settings.algo_allow_margin
    report_interval = settings.server_report_interval_sec
    if report is None:
        open_positions = {}
        open_orders = {}
        candidates_live = {}
    else:
        report.reported_text = report.report_time.strftime("%d %b %H:%M:%S")
        if report.started_time is not None:
            report.started_time_text = report.started_time.strftime("%d %b %H:%M:%S")
        else:
            report.started_time_text = '---------------------'
        report.last_worker_execution_text = report.last_worker_execution.strftime("%H:%M:%S")
        report.market_time_text = report.market_time.strftime("%H:%M")
        report.dailyPnl = round(report.dailyPnl, 2)
        pnl_bg_box_color = 'bg-love-kiss' if report.dailyPnl < 0 else 'bg-grow-early'
        report.remaining_sma_with_safety = round(report.remaining_sma_with_safety, 2)

        open_positions = json.loads(report.open_positions_json)
        open_orders = json.loads(report.open_orders_json)
        report.all_positions_value = 0
        sectors_dict = {}
        for k, v in open_positions.items():
            position = Position.query.filter_by(email=current_user.email, last_exec_side='BOT', ticker=k).first()
            if position is not None:
                delta = datetime.today() - position.opened
                v['days_open'] = delta.days
            else:
                v['days_open'] = 0

            profit = v['UnrealizedPnL'] / v['Value'] * 100 if v['Value'] != 0 else 0
            v['profit_in_percents'] = profit
            if v['stocks'] != 0:
                report.all_positions_value += int(v['Value'])
                v['last_bid'] = v['Value'] / v['stocks']
            if profit > 0:
                v['profit_class'] = 'text-success'
                v['profit_progress_colour'] = 'bg-success'
                v['profit_progress_percent'] = profit / 6 * 100
            else:
                v['profit_class'] = 'text-danger'
                v['profit_progress_colour'] = 'bg-danger'
                v['profit_progress_percent'] = abs(profit / 10 * 100)

            candidate = Candidate.query.filter_by(ticker=k).first()
            sectors_dict[candidate.sector] = sectors_dict[candidate.sector] + int(v['Value']) if candidate.sector in sectors_dict.keys() else int(v['Value'])

        graph_sectors = []
        graph_sectors_values = []
        for sec, val in sectors_dict.items():
            graph_sectors.append(sec)
            graph_sectors_values.append(val)

        if not use_margin:
            report.excess_liquidity = round(report.net_liquidation - report.all_positions_value, 1)

        candidates_live = json.loads(report.candidates_live_json)
        for k, v in candidates_live.items():
            if 'target_price' not in v.keys():
                v['target_price'] = 0

        online = general.user_online_status(report.report_time, settings.station_interval_worker_sec)
        api_error = False if report.api_connected else True

    trading_session_state = is_market_open()
    current_est_time = general.get_by_timezone('US/Eastern').time().strftime("%H:%M")
    if report is not None:
        report.pnl_percent=round(report.dailyPnl/report.net_liquidation*100,2)

    if report is None:
        return redirect(url_for('candidates.usercandidates'))
    else:
        return render_template('userview/traderstationstate.html',
                               graph_sectors=graph_sectors,
                               graph_sectors_values=graph_sectors_values,
                               current_est_time=current_est_time,
                               online=online,
                               api_error=api_error,
                               trading_session_state=trading_session_state,
                               report_interval=report_interval,
                               report_time=report.report_time,
                               candidates_live=candidates_live,
                               open_positions=open_positions,
                               open_orders=open_orders,
                               user=current_user,
                               report=report,
                               margin_used=use_margin,
                               pnl_bg_box_color=pnl_bg_box_color,
                               last_update_date=last_update.last_update_date.strftime("%d %b %H:%M"),
                               bg_upd_color=bg_upd_color,
                               form=None)


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


@userview.route('closedpositions', methods=['GET', 'POST'])
@login_required
def closedpositions():
    if not current_user.admin_confirmed or not current_user.signature:
        return redirect(url_for('station.download'))

    filter_radio = '1'
    max_date = datetime.now().date() #datetime.now(pytz.timezone('America/Lima')) ##from tzlocal import get_localzone # $ pip install tzlocal
    min_date = db.session.query(ReportStatistic).filter(ReportStatistic.email == current_user.email).order_by(ReportStatistic.report_time).first().report_time
    min_date = min_date if min_date is not None else datetime.now() + relativedelta(years=1)
    from_date = min_date
    to_date = datetime.now() + relativedelta(days=1)

    if request.method == 'POST':
        from_date = request.form['from_date']
        to_date_str = request.form['to_date']
        to_date = datetime.strptime(to_date_str, '%Y-%m-%d') + relativedelta(days=1)
        filter_radio = request.form['filter_radio']

    closed_positions = Position.query.filter(Position.email == current_user.email,
                                             Position.last_exec_side == 'SLD',
                                             Position.closed.between(from_date, to_date)).all()

    reports_min_max = db.session.query(db.func.min(ReportStatistic.report_time), db.func.max(ReportStatistic.report_time))\
        .filter(ReportStatistic.email == current_user.email,
                ReportStatistic.report_time.between(from_date, to_date),
                ReportStatistic.net_liquidation != 0).first()

    reports = ReportStatistic.query.filter(ReportStatistic.email == current_user.email) \
        .filter(or_(ReportStatistic.report_time == reports_min_max[0],
                    ReportStatistic.report_time == reports_min_max[1])).all()

    if reports is not None and len(reports) > 0:
        profit_usd = reduce(lambda x, y: y - x, list(map(lambda z: z.net_liquidation, reports)))
        profit_procent = profit_usd / reports[0].net_liquidation * 100
        profit_class = "text-success" if profit_usd > 0 else "text-danger"
    else:
        profit_usd = 0
        profit_procent = 0
        profit_class = ""

    if closed_positions is not None and len(closed_positions) > 0:
        succeed_positions = [p for p in closed_positions if p.profit > 0]
        failed_positions = [p for p in closed_positions if p.profit < 0]
    else:
        succeed_positions = []
        failed_positions = []

    for c in closed_positions:
        delta = c.closed - c.opened
        c.days_in_action = delta.days
    return render_template('userview/closedpositions.html',
                           positions=closed_positions,
                           user=current_user.email,
                           filter_radio=filter_radio,
                           min_date=min_date.strftime("%Y-%m-%d"),
                           max_date=max_date.strftime("%Y-%m-%d"),
                           from_date=from_date,
                           to_date=to_date + relativedelta(days=-1),
                           profit_usd=profit_usd,
                           profit_procent=profit_procent,
                           count_positions=len(closed_positions),
                           succeed_positions=len(succeed_positions),
                           failed_positions=len(failed_positions),
                           profit_class=profit_class,
                           form=None)


@userview.route('portfoliostatistics', methods=['GET', 'POST'])
@login_required
def portfoliostatistics():
    """Display a user's account information."""
    return render_template('userview/portfoliostatistics.html', user=current_user, form=None)
