import json

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

from app import db
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
from app.models import User, Position, Report

userview = Blueprint('userview', __name__)





@userview.route('traderstationstate', methods=['GET', 'POST'])
@login_required
def traderstationstate():

    report = Report.query.filter_by(email=current_user.email).first()
    report.reported_text=report.report_time.strftime("%Y-%m-%d %H:%M:%S")
    report.last_worker_execution_text=report.last_worker_execution.strftime("%Y-%m-%d %H:%M:%S")
    report.market_time_text = report.market_time.strftime("%Y-%m-%d %H:%M:%S")
    report.dailyPnl=round(report.dailyPnl,2)

    open_positions = json.loads(report.open_positions_json)
    for k,v in open_positions.items():
        profit=v['UnrealizedPnL']/v['Value']*100
        v['profit_in_percents']=profit

        if profit>0:
            v['profit_class'] = 'text-success'
            v['profit_progress_colour'] = 'bg-success'
            v['profit_progress_percent'] = profit / 6 * 100
        else:
            v['profit_class'] = 'text-danger'
            v['profit_progress_colour'] = 'bg-danger'
            v['profit_progress_percent'] = abs(profit / 10 * 100)
    return render_template('userview/traderstationstate.html',open_positions=open_positions, user=current_user,report=report, form=None)

@userview.route('closedpositions', methods=['GET', 'POST'])
@login_required
def closedpositions():
    """Display a user's account information."""
    closed_positions = Position.query.all()
    return render_template('userview/closedpositions.html', user=current_user,positions=closed_positions, form=None)

@userview.route('portfoliostatistics', methods=['GET', 'POST'])
@login_required
def portfoliostatistics():
    """Display a user's account information."""
    return render_template('userview/portfoliostatistics.html', user=current_user, form=None)

@userview.route('usercandidates', methods=['GET', 'POST'])
@login_required
def usercandidates():
    """Display a user's account information."""
    return render_template('userview/usercandidates.html', user=current_user, form=None)