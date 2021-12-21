import json
from flask import (
    Blueprint,
    request
)

from app import csrf
from app.models import db_service, ReportStatistic, Report, ProcessStatus, UserSetting, NotificationProcess
from datetime import datetime
import app.generalutils as general
import app.enums as enum

research = Blueprint('research', __name__)


@csrf.exempt
@research.route('/update_reports_statistic', methods=['GET'])
def update_reports_statistic():
    try:
        reports = Report.query.all()
        for r in reports:
            snapshot = ReportStatistic()
            snapshot.email = r.email
            snapshot.report_time = r.report_time
            snapshot.snapshot_time = datetime.utcnow()
            snapshot.net_liquidation = r.net_liquidation
            snapshot.remaining_sma_with_safety = r.remaining_sma_with_safety
            snapshot.remaining_trades = r.remaining_trades
            snapshot.all_positions_value = r.all_positions_value
            snapshot.open_positions_json = r.open_positions_json
            snapshot.open_orders_json = r.open_orders_json
            snapshot.dailyPnl = r.dailyPnl
            snapshot.last_worker_execution = r.last_worker_execution
            snapshot.market_time = r.market_time
            snapshot.market_state = r.market_state
            snapshot.excess_liquidity = r.excess_liquidity
            snapshot.candidates_live_json = r.candidates_live_json
            snapshot.started_time = r.started_time
            snapshot.api_connected = r.api_connected
            snapshot.market_data_error = r.market_data_error
            snapshot.add_report()
        return "successfully update reports statistic"
    except:
        print('problem with update reports statistic')
        return "update reports statistic failed"


@research.route('/get_tooltips',  methods=['GET'])
@csrf.exempt
def get_tooltips():
    tooltips = db_service.get_tooltips()
    return json.dumps(tooltips, cls=general.JsonEncoder)


@csrf.exempt
@research.route('/update_process_status', methods=['POST'])
def update_process_status():
    status = int(request.form['status'])
    percent = float(request.form['percent'])

    try:
        process_status = ProcessStatus.query.filter_by(process_type=enum.ProcessType.NOTIFICATIONS.value).first()
        if process_status is None:
            process_status = ProcessStatus()
            process_status.process_type = enum.ProcessType.NOTIFICATIONS.value
        if status == 0:
            process_status.start_process_date = datetime.utcnow()
            process_status.status = "process started"
            process_status.percent = 0
        elif status == 1:
            process_status.status = "process run"
            process_status.percent = percent
        else:
            process_status.status = "process finished"
            process_status.percent = 100
        process_status.update_status()
        return "successfully update process status"
    except Exception as e:
        print('problem with update process status. ', e)
        return "failed to update process status"


@csrf.exempt
@research.route('/all_users_for_notifications', methods=['GET'])  # for use from the task
def all_users_for_notifications():
    users = UserSetting.query.filter_by(notify_candidate_signal=1).all()
    resp = []
    for u in users:
        resp.append(u.email)
    return json.dumps(resp)


@csrf.exempt
@research.route('/save_process_data', methods=['POST'])
def save_process_data():
    error_status = request.form['error_status']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    num_of_users = request.form['num_of_users']
    num_users_received = request.form['num_users_received']
    avg_update_times = request.form['avg_update_times']

    now = datetime.utcnow()
    try:
        last_update_data = NotificationProcess.query.order_by(NotificationProcess.start_process_time.desc()).first()
        update_data = NotificationProcess()
        if error_status == '1':
            update_data.error_status = True
            update_data.last_update_date = last_update_data.last_update_date if last_update_data is not None else now
        else:
            update_data.last_update_date = end_time
            update_data.error_status = False
        update_data.start_process_time = start_time
        update_data.end_process_time = end_time
        update_data.avg_time_by_position = avg_update_times
        update_data.num_of_users = num_of_users
        update_data.num_users_received = num_users_received
        update_data.update_data()
        return "successfully update date"
    except Exception as e:
        print('problem with update last date. ', e)
        return "failed to update date"






