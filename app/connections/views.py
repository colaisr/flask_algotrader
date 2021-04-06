import json

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from datetime import datetime
from app import db, csrf
from app.models import User, Connection, Report, Position, ClientCommand, UserSetting, TickerData, \
    Candidate

connections = Blueprint('connections', __name__)


@csrf.exempt
@connections.route('/logconnection', methods=['POST'])
def logconnection():
    request_data = request.get_json()
    logged_user = request_data["user"]
    users = User.query.all()
    if any(x.email == logged_user for x in users):
        c = Connection()
        c.email = logged_user
        now = datetime.now()
        c.reported_connection = now
        c.log_connection()
        return "Application launch for " + logged_user + " is logged."
    else:
        return "The user configured is not found on Server the connection is not logged"


def filter_add_data(requested_candidates,logged_user):
    user_settings = UserSetting.query.filter_by(email=logged_user).first()

    filtered_tipranks=[]
    for c in requested_candidates:
        td=TickerData.query.filter_by(ticker=c.ticker).order_by(TickerData.updated_server_time.desc()).first()
        if user_settings.algo_apply_min_rank:
            if td.tipranks>=user_settings.algo_min_rank:
                filtered_tipranks.append(td)
        else:
            filtered_tipranks.append(td)

    filtered_scores=[]
    for f in filtered_tipranks:
        if user_settings.algo_apply_accepted_fmp_ratings:
            allowed=user_settings.algo_accepted_fmp_ratings.split(',')
            if f.fmp_rating in allowed:
                filtered_scores.append(f)
        else:
            filtered_scores.append(f)
    return filtered_scores


def retrieve_user_candidates(user):
    requested_for_user = user
    user_candidates=Candidate.query.filter_by(email=requested_for_user,enabled=True).all()
    user_settings = UserSetting.query.filter_by(email=requested_for_user).first()

    if user_settings.server_use_system_candidates:
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
    requested_candidates=filter_add_data(requested_candidates,requested_for_user)
    cand_dictionaries=[]
    for c in requested_candidates:
        cand_dictionaries.append(c.toDictionary())
    return cand_dictionaries


@csrf.exempt
@connections.route('/postreport', methods=['POST'])
def logreport():
    request_data = request.get_json()
    logged_user = request_data["user"]
    users = User.query.all()
    if any(x.email == logged_user for x in users):
        report = Report()
        report.email = logged_user
        now = datetime.now()
        report.report_time =datetime.fromisoformat(request_data["report_time"])
        report.remaining_trades = request_data["remaining_trades"]
        report.open_positions_json = request_data["open_positions"]
        report.open_orders_json = request_data["open_orders"]
        report.candidates_live_json=request_data["candidates_live"]
        report.all_positions_value = request_data["all_positions_value"]
        report.net_liquidation = request_data["net_liquidation"]
        report.remaining_sma_with_safety = request_data["remaining_sma_with_safety"]
        report.excess_liquidity=request_data["excess_liquidity"]
        report.dailyPnl = request_data["dailyPnl"]
        report.last_worker_execution =datetime.fromisoformat(request_data["last_worker_run"])
        report.market_time =datetime.fromisoformat(request_data["market_time"])
        report.market_state = request_data["market_state"]
        report.update_report()

        return "Report snapshot stored at server"
    else:
        return "The user configured is not found on Server the report is not logged"

@csrf.exempt
@connections.route('/getcommand', methods=['POST'])
def get_command():
    request_data = request.get_json()
    logged_user = request_data["user"]
    users = User.query.all()
    if any(x.email == logged_user for x in users):
        response={}
        client_command = ClientCommand.query.filter_by(email=logged_user).first()
        response['command']=client_command.command
        response['candidates']=retrieve_user_candidates(logged_user)
        if client_command.command=='restart_worker':
            client_command.set_run_worker()
        return response
    else:
        return "The user configured is not found on Server the report is not logged"

@csrf.exempt
@connections.route('logrestartrequest/', methods=['POST'])
def log_restart_request():
    logged_user=request.form['usersemail']
    client_command = ClientCommand.query.filter_by(email=logged_user).first()
    client_command.set_restart()
    flash('Restart request logged', 'success')
    return redirect(url_for('userview.traderstationstate'))


@csrf.exempt
@connections.route('/postexecution', methods=['POST'])
def postexecution():
    request_data = request.get_json()
    logged_user = request_data["user"]
    symbol = request_data["symbol"]
    shares = request_data["shares"]
    price = request_data["price"]
    side = request_data["side"]
    reported_time=json.loads(request_data['time'])
    time = datetime.fromisoformat(reported_time)

    users = User.query.all()
    if any(x.email == logged_user for x in users):
        position = Position()
        if side=='BOT':
            position.ticker=symbol
            position.email=logged_user
            position.stocks=shares
            position.last_exec_side=side
            position.open_price=price
            position.opened=time
        else:
            position.ticker=symbol
            position.email=logged_user
            position.stocks=shares
            position.last_exec_side=side
            position.close_price=price
            position.closed=time
        position.update_position()
        return "Execution for " + logged_user + " stored at server."
    else:
        return "The user configured is not found on Server the execution is not logged"