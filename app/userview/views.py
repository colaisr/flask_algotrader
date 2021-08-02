import json
import ssl
from datetime import datetime, timedelta, time
from urllib.request import urlopen

import pytz
from pytz import timezone

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_rq import get_queue

from app import db, csrf
from app.account.forms import (
    ChangeEmailForm,
    ChangePasswordForm,
    CreatePasswordForm,
    LoginForm,
    RegistrationForm,
    RequestResetPasswordForm,
    ResetPasswordForm,
)
from app.email import send_email
from app.models import User, Position, Report, Candidate, UserSetting

userview = Blueprint('userview', __name__)

def is_market_open():
    url = ('https://financialmodelingprep.com/api/v3/is-the-market-open?apikey=f6003a61d13c32709e458a1e6c7df0b0')
    state='Error'
    try:
        context = ssl._create_unverified_context()
        response = urlopen(url, context=context)
        data = response.read().decode("utf-8")
        parsed=json.loads(data)
        state=parsed['isTheStockMarketOpen']
        if state:
            state="Open"
        else:
            state="Closed"
    except:
        y=3
    return state

@userview.route('traderstationstate', methods=['GET', 'POST'])
@login_required
def traderstationstate():
    re=request
    report = Report.query.filter_by(email=current_user.email).first()
    settings=UserSetting.query.filter_by(email=current_user.email).first()
    use_margin=settings.algo_allow_margin
    report_interval=settings.server_report_interval_sec
    if report is None:
        #report=Report()
        open_positions={}
        open_orders={}
        candidates_live={}
        i=3
    else:
        report.reported_text=report.report_time.strftime("%m-%d %H:%M:%S")
        if report.started_time !=None:
            report.started_time_text = report.started_time.strftime("%m-%d %H:%M:%S")
        else:
            report.started_time_text ='---------------------'
        report.last_worker_execution_text=report.last_worker_execution.strftime("%H:%M:%S")
        report.market_time_text = report.market_time.strftime("%H:%M")
        report.dailyPnl=round(report.dailyPnl,2)
        report.remaining_sma_with_safety = round(report.remaining_sma_with_safety, 2)

        open_positions = json.loads(report.open_positions_json)
        open_orders = json.loads(report.open_orders_json)
        report.all_positions_value=0
        sectors_dict={}
        for k,v in open_positions.items():
            position = Position.query.filter_by(email=current_user.email, last_exec_side='BOT',ticker=k).first()
            if position != None:
                delta=datetime.today()-position.opened
                v['days_open']=delta.days
            else:
                v['days_open'] = "many"

            if v['Value'] !=0:
                profit=v['UnrealizedPnL']/v['Value']*100
            else:
                profit=0
            v['profit_in_percents']=profit
            if v['stocks'] !=0:
                report.all_positions_value+=int(v['Value'])
                v['last_bid']=v['Value']/v['stocks']
            if profit>0:
                v['profit_class'] = 'text-success'
                v['profit_progress_colour'] = 'bg-success'
                v['profit_progress_percent'] = profit / 6 * 100
            else:
                v['profit_class'] = 'text-danger'
                v['profit_progress_colour'] = 'bg-danger'
                v['profit_progress_percent'] = abs(profit / 10 * 100)

            candidate = Candidate.query.filter_by(ticker=k).first()
            if candidate.sector in sectors_dict.keys():
                sectors_dict[candidate.sector]=sectors_dict[candidate.sector]+int(v['Value'])
            else:
                sectors_dict[candidate.sector] =int(v['Value'])
        graph_sectors=[]
        graph_sectors_values=[]
        for sec,val in sectors_dict.items():
            graph_sectors.append(sec)
            graph_sectors_values.append(val)



        if not use_margin:
            report.excess_liquidity=round(report.net_liquidation-report.all_positions_value,1)

        candidates_live = json.loads(report.candidates_live_json)
        for k, v in candidates_live.items():
            if 'target_price' not in v.keys():
                v['target_price']=0

        report_time=report.report_time
        current=datetime.utcnow()
        #
        # aware=pytz.utc.localize(report_time)
        # tz = timezone('Europe/Moscow')
        # moscow_time=datetime.now(tz)
        delta= (current-report_time).seconds
        refresh_rate=settings.station_interval_worker_sec*2 #takes time to process
        if delta<refresh_rate:
            online=True
        else:
            online=False

        if report.api_connected:
            api_error=False
        else:
            api_error=True

    trading_session_state=is_market_open()
    tz = timezone('US/Eastern')
    current_est_time=datetime.now(tz).time().strftime("%H:%M")

    if report is None:
        return redirect(url_for('candidates.usercandidates'))
    else:
        return render_template('userview/traderstationstate.html',graph_sectors=graph_sectors,graph_sectors_values=graph_sectors_values,current_est_time=current_est_time,online=online,api_error=api_error,trading_session_state=trading_session_state,report_interval=report_interval,report_time=report_time,candidates_live=candidates_live,open_positions=open_positions,open_orders=open_orders, user=current_user,report=report,margin_used=use_margin, form=None)

# def check_session_state(): #changed to FMP API
#     tz = timezone('US/Eastern')
#     current_est_time=datetime.now(tz).time()
#     dstart = time(4, 0, 0)
#     dend=time(20, 0, 0)
#     tstart=time(9, 30, 0)
#     tend=time(16, 0, 0)
#     if time_in_range(dstart,tstart,current_est_time):
#         return "Pre Market"
#     elif time_in_range(tstart,tend,current_est_time):
#         return "Open"
#     elif time_in_range(tend,dend,current_est_time):
#         return "After Market"
#     else:
#         return "Closed"


def time_in_range(start, end, x):
    """Return true if x is in the range [start, end]"""
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end


@userview.route('closedpositions', methods=['GET', 'POST'])
@login_required
def closedpositions():
    closed_positions = Position.query.filter_by(email=current_user.email,last_exec_side='SLD').all()
    for c in closed_positions:
        delta=c.closed-c.opened
        c.days_in_action=delta.days
    return render_template('userview/closedpositions.html',positions=closed_positions, form=None)

@userview.route('portfoliostatistics', methods=['GET', 'POST'])
@login_required
def portfoliostatistics():
    """Display a user's account information."""
    return render_template('userview/portfoliostatistics.html', user=current_user, form=None)

