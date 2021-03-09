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
        report=Report()
        open_positions={}
        open_orders={}
    else:
        report.reported_text=report.report_time.strftime("%Y-%m-%d %H:%M:%S")
        report.last_worker_execution_text=report.last_worker_execution.strftime("%Y-%m-%d %H:%M:%S")
        report.market_time_text = report.market_time.strftime("%Y-%m-%d %H:%M:%S")
        report.dailyPnl=round(report.dailyPnl,2)
        report.remaining_sma_with_safety = round(report.remaining_sma_with_safety, 2)

        open_positions = json.loads(report.open_positions_json)
        open_orders = json.loads(report.open_orders_json)
        for k,v in open_positions.items():

            if v['Value'] !=0:
                profit=v['UnrealizedPnL']/v['Value']*100
                report.all_positions_value+=v['Value']
            else:
                profit=0
            v['profit_in_percents']=profit

            if profit>0:
                v['profit_class'] = 'text-success'
                v['profit_progress_colour'] = 'bg-success'
                v['profit_progress_percent'] = profit / 6 * 100
            else:
                v['profit_class'] = 'text-danger'
                v['profit_progress_colour'] = 'bg-danger'
                v['profit_progress_percent'] = abs(profit / 10 * 100)
    return render_template('userview/traderstationstate.html',open_positions=open_positions,open_orders=open_orders, user=current_user,report=report,margin_used=use_margin, form=None)

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

@userview.route('usercandidates', methods=['GET', 'POST'])
@login_required
def usercandidates():
    candidates=Candidate.query.filter_by(email=current_user.email).all()
    return render_template('userview/usercandidates.html',candidates=candidates, user=current_user, form=None)

@userview.route('updatecandidate/', methods=['POST'])
@csrf.exempt
def updatecandidate():

    c=Candidate()
    c.ticker=request.form['txt_ticker']
    c.description=request.form['txt_description']
    c.email=current_user.email
    c.update_candidate()
    c.enabled=True
    return redirect(url_for('userview.usercandidates'))

@userview.route('removecandidate/', methods=['POST'])
@csrf.exempt
def removecandidate():
    ticker=request.form['ticker_to_remove']
    candidate = Candidate.query.filter_by(email=current_user.email,ticker=ticker).first()
    candidate.delete_candidate()
    return redirect(url_for('userview.usercandidates'))

@userview.route('enabledisable/', methods=['POST'])
@csrf.exempt
def enabledisable():
    ticker=request.form['ticker_to_change']
    candidate = Candidate.query.filter_by(email=current_user.email,ticker=ticker).first()
    candidate.change_enabled_state()
    return redirect(url_for('userview.usercandidates'))

@csrf.exempt
@userview.route('/retrieveusercandidates', methods=['GET'])
def retrievecandidates():
    request_data = request.get_json()
    use_system_candidates=request_data["use_system_candidates"]
    logged_user = request_data["user"]
    user_candidates=Candidate.query.filter_by(email=logged_user,enabled=True).all()
    if use_system_candidates:
        admin_candidates=Candidate.query.filter_by(email='admin@gmail.com',enabled=True).all()
        for uc in user_candidates:
            for ac in admin_candidates:
                if ac.ticker == uc.ticker:
                    print("i found it!")
                    break
            else:
                admin_candidates.append(uc)
        requested_candidates=admin_candidates
    else:
        requested_candidates=user_candidates
    cand_dictionaries=[]
    for c in requested_candidates:
        cand_dictionaries.append(c.to_dictionary())
    response=json.dumps(cand_dictionaries)




    return response