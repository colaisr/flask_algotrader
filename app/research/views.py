import json
from flask import (
    Blueprint,
    request
)

from app import csrf
from app.models import db_service, ReportStatistic, Report, ProcessStatus, UserSetting
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






