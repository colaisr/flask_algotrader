import json
import time

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from datetime import datetime

from sqlalchemy import text
from sqlalchemy.orm import sessionmaker

from app import db, csrf
from app.email import send_email
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

    query_text="select a.* from Tickersdata a join (  select Tickersdata.`ticker`, max(Tickersdata.`updated_server_time`) as updated_server_time  from Tickersdata group by Tickersdata.`ticker`) b on b.`ticker`=a.`ticker` and b.`updated_server_time`=a.`updated_server_time`"
    uniq_tickers_data=db.session.query(TickerData).from_statement(text(query_text)).all()

    related_tds=[]
    for c in requested_candidates:
        adding = list(filter(lambda td: td.ticker == c.ticker, uniq_tickers_data))
        if len(adding)==0:
            # missed bringing a market data
            b=3
        else:
            related_tds.append(adding[0])

    if user_settings.algo_apply_min_rank:
        filtered_tipranks = list(filter(lambda td: td.tipranks >= user_settings.algo_min_rank, related_tds))
    else:
        filtered_tipranks=related_tds

    if user_settings.algo_apply_accepted_fmp_ratings:
        allowed = user_settings.algo_accepted_fmp_ratings.split(',')
        filtered_scores = list(filter(lambda td: td.fmp_rating in allowed, filtered_tipranks))
    else:
        filtered_scores=filtered_tipranks

    if user_settings.algo_apply_max_yahoo_rank:
        filtered_yahoo_ranks = list(filter(lambda td: td.yahoo_rank < user_settings.algo_max_yahoo_rank, filtered_scores))
    else:
        filtered_yahoo_ranks=filtered_scores
    return filtered_yahoo_ranks

def sort_by_parameter_desc(object,property):
    return sorted(object, key=lambda x: x[property], reverse=True)

def sort_candidates(cand_dictionaries):
    sorted_momentum=sort_by_parameter_desc(cand_dictionaries,'twelve_month_momentum')
    sorted_underprice = sort_by_parameter_desc(sorted_momentum, 'under_priced_pnt')
    sorted_yahooo = sort_by_parameter_desc(sorted_momentum, 'yahoo_rank')
    sorted_tiprank=sort_by_parameter_desc(sorted_yahooo,'tipranks')
    return sorted_tiprank


def retrieve_user_candidates(user):
    requested_for_user = user
    user_candidates=Candidate.query.filter_by(email=requested_for_user,enabled=True).all()
    user_settings = UserSetting.query.filter_by(email=requested_for_user).first()

    if user_settings.server_use_system_candidates:
        admin_candidates=Candidate.query.filter_by(email='admin@gmail.com',enabled=True).all()
        for uc in user_candidates:
            for ac in admin_candidates:
                if ac.ticker == uc.ticker:
                    break
            else:
                admin_candidates.append(uc)
        requested_candidates=admin_candidates
    else:
        requested_candidates=user_candidates
    requested_candidates=filter_add_data(requested_candidates,requested_for_user)
    # requested_candidates.sort(key=sort_by_tiprank)
    # requested_candidates=requested_candidates[:85]    #trader station allow to track only 100
    cand_dictionaries=[]
    for c in requested_candidates:
        cand_dictionaries.append(c.toDictionary())
    sorted_list=sort_candidates(cand_dictionaries)
    return sorted_list

def sort_by_tiprank(e):
  return e.tipranks

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
        report.started_time = datetime.fromisoformat(request_data["started_time"])
        report.update_report()

        return "Report snapshot stored at server"
    else:
        return "The user configured is not found on Server the report is not logged"


def retrieve_user_positions(logged_user):
    open_positions = Position.query.filter_by(last_exec_side='BOT',email=logged_user)
    open_positions_dictionaries = []
    for c in open_positions:
        open_positions_dictionaries.append(c.toDictionary())
    return open_positions_dictionaries


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
        response['open_positions'] = retrieve_user_positions(logged_user)
        if client_command.command=='restart_worker':
            client_command.set_run_worker()
        elif client_command.command=='close_all_positions':
            client_command.set_run_worker()
        return response
    else:
        return "The user configured is not found on Server the report is not logged"

# @csrf.exempt
# @connections.route('/getopenpositions', methods=['POST'])
# def get_open_positions():
#     request_data = request.get_json()
#     logged_user = request_data["user"]
#     users = User.query.all()
#     if any(x.email == logged_user for x in users):
#         response={}
#         open_positions=Position.query.filter_by(last_exec_side='BOT')
#         open_positions_dictionaries = []
#         for c in open_positions:
#             open_positions_dictionaries.append(c.toDictionary())
#         response['open_positions'] =open_positions_dictionaries
#         return response
#     else:
#         return "The user configured is not found on Server the report is not logged"

@csrf.exempt
@connections.route('logrestartrequest/', methods=['POST'])
def log_restart_request():
    logged_user=request.form['usersemail']
    client_command = ClientCommand.query.filter_by(email=logged_user).first()
    client_command.set_restart()
    flash('Restart request logged', 'success')
    return redirect(url_for('userview.traderstationstate'))

@csrf.exempt
@connections.route('restart_all_stations', methods=['POST'])
def restart_all_stations():
    clients = ClientCommand.query.all()
    for c in clients:
        c.set_restart()
    return "all stations booked to restart"


def check_if_market_fall(logged_user):
    user_settings = UserSetting.query.filter_by(email=logged_user).first()
    if user_settings.algo_sell_on_swan==False:
        return
    else:
        today = datetime.today().date()
        today_closings = Position.query.filter(Position.email == logged_user, Position.last_exec_side == 'SLD',
                                               Position.closed >= today,Position.profit<0).all()
        if len(today_closings)>user_settings.algo_positions_for_swan:
            #more than 3 positions closed same day on profit negative - stop buying option and notify
            user_settings = UserSetting.query.filter_by(email=logged_user).first()
            user_settings.algo_allow_buy=False
            user_settings.update_user_settings()
            send_email(recipient=logged_user,
                subject='Algotrader: Black Swan is suspected!',
                template='account/email/position_open')

            client_command = ClientCommand.query.filter_by(email=logged_user).first()
            client_command.set_close_all_positions()


def notify_open(position, logged_user):
    user_settings = UserSetting.query.filter_by(email=logged_user).first()
    if user_settings.notify_buy:
        send_email(recipient=logged_user,
                   subject='Algotrader: new position is open for '+position.ticker,
                   template='account/email/position_open',
                   position=position)


def notify_closed(position, logged_user):
    user_settings = UserSetting.query.filter_by(email=logged_user).first()

    if user_settings.notify_sell:
        if position.profit>0:
            text_for_message='Algotrader: closed position for ' + position.ticker+" with Profit"
        else:
            text_for_message = 'Algotrader: closed position for ' + position.ticker + "with Loss"
        send_email(recipient=logged_user,
                   subject=text_for_message,
                   template='account/email/position_close',
                   position=position)


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
            result,np = position.update_position()
        else:
            position.ticker=symbol
            position.email=logged_user
            position.stocks=shares
            position.last_exec_side=side
            position.close_price=price
            position.closed=time
            result,np=position.update_position()
        if result=="new_sell":
            check_if_market_fall(logged_user)
            notify_closed(np, logged_user)
        elif result=="new_buy":
            notify_open(np,logged_user)

        return "Execution for " + logged_user + " stored at server."
    else:
        return "The user configured is not found on Server the execution is not logged"