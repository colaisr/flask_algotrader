import json
from datetime import datetime

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

@userview.route('traderstationstate', methods=['GET', 'POST'])
@login_required
def traderstationstate():

    report = Report.query.filter_by(email=current_user.email).first()
    settings=UserSetting.query.filter_by(email=current_user.email).first()
    use_margin=settings.algo_allow_margin
    if report is None:
        #report=Report()
        open_positions={}
        open_orders={}
        candidates_live={}
        i=3
    else:
        report.reported_text=report.report_time.strftime("%Y-%m-%d %H:%M:%S")
        report.last_worker_execution_text=report.last_worker_execution.strftime("%Y-%m-%d %H:%M:%S")
        report.market_time_text = report.market_time.strftime("%Y-%m-%d %H:%M:%S")
        report.dailyPnl=round(report.dailyPnl,2)
        report.remaining_sma_with_safety = round(report.remaining_sma_with_safety, 2)

        open_positions = json.loads(report.open_positions_json)
        open_orders = json.loads(report.open_orders_json)
        report.all_positions_value=0
        for k,v in open_positions.items():

            if v['Value'] !=0:
                profit=v['UnrealizedPnL']/v['Value']*100
            else:
                profit=0
            v['profit_in_percents']=profit
            if v['stocks'] !=0:
                report.all_positions_value+=int(v['Value'])
            if profit>0:
                v['profit_class'] = 'text-success'
                v['profit_progress_colour'] = 'bg-success'
                v['profit_progress_percent'] = profit / 6 * 100
            else:
                v['profit_class'] = 'text-danger'
                v['profit_progress_colour'] = 'bg-danger'
                v['profit_progress_percent'] = abs(profit / 10 * 100)

        if not use_margin:
            report.excess_liquidity=round(report.net_liquidation-report.all_positions_value,1)

        candidates_live = json.loads(report.candidates_live_json)

        report_time=report.report_time

    if report is None:
        return redirect(url_for('candidates.usercandidates'))
    else:
        return render_template('userview/traderstationstate.html',report_time=report_time,candidates_live=candidates_live,open_positions=open_positions,open_orders=open_orders, user=current_user,report=report,margin_used=use_margin, form=None)

@userview.route('closedpositions', methods=['GET', 'POST'])
@login_required
def closedpositions():
    """Display a user's account information."""
    closed_positions = Position.query.filter_by(email=current_user.email,last_exec_side='SLD').all()
    return render_template('userview/closedpositions.html',positions=closed_positions, form=None)

@userview.route('portfoliostatistics', methods=['GET', 'POST'])
@login_required
def portfoliostatistics():
    """Display a user's account information."""
    return render_template('userview/portfoliostatistics.html', user=current_user, form=None)

