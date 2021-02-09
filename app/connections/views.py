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
from app.models import User, Connection, Report

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
        report = Report.query.filter_by(email=logged_user).first()
        if report is None:
            report = Report()
        report.email = logged_user
        now = datetime.now()
        report.report_time = now
        report.remaining_trades = request_data["remaining_trades"]
        report.open_positions_json = request_data["open_positions"]
        report.open_orders_json = request_data["open_orders"]
        report.all_positions_value = request_data["all_positions_value"]
        report.net_liquidation = request_data["net_liquidation"]
        report.remaining_sma_with_safety = request_data["remaining_sma_with_safety"]
        report.dailyPnl = request_data["dailyPnl"]
        report.log_report()


        return "Report for " + logged_user + " stored at server."
    else:
        return "The user configured is not found on Server the report is not logged"
