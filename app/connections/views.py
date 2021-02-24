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
from app.models import User, Connection, Report, Position

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
        report.all_positions_value = request_data["all_positions_value"]
        report.net_liquidation = request_data["net_liquidation"]
        report.remaining_sma_with_safety = request_data["remaining_sma_with_safety"]
        report.dailyPnl = request_data["dailyPnl"]
        report.last_worker_execution =datetime.fromisoformat(request_data["last_worker_run"])
        report.market_time =datetime.fromisoformat(request_data["market_time"])
        report.market_state = request_data["market_state"]

        report.update_report()
        return "Report snapshot for " + logged_user + " stored at server."
    else:
        return "The user configured is not found on Server the report is not logged"


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