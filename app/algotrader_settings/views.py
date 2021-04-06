import json
from flask import (
    Blueprint,
    render_template,
    request, url_for
)
from datetime import datetime, date, timedelta

from flask_login import login_required, current_user

from werkzeug.utils import redirect


from app import db, csrf
from app.models import UserSetting

algotradersettings = Blueprint('algotradersettings', __name__)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

@algotradersettings.route('/usersettings', methods=['GET'])
@login_required
def usersettings():
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()
    return render_template('userview/algotraderSettings.html',user_settings=user_settings)

@algotradersettings.route('/savesettings', methods=['POST'])
@login_required
def savesettings():
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()
    user_settings.algo_max_loss=request.form['algo_max_loss']
    user_settings.algo_take_profit = request.form['algo_take_profit']
    user_settings.algo_bulk_amount_usd = request.form['algo_bulk_amount_usd']
    user_settings.algo_trailing_percent = request.form['algo_trailing_percent']
    if "algo_apply_accepted_fmp_ratings" in request.form.keys():
        user_settings.algo_apply_accepted_fmp_ratings = True
    else:
        user_settings.algo_apply_accepted_fmp_ratings =False
    user_settings.algo_accepted_fmp_ratings = request.form['algo_accepted_fmp_ratings']
    if "algo_allow_buy" in request.form.keys():
        user_settings.algo_allow_buy = True
    else:
        user_settings.algo_allow_buy=False

    if "algo_allow_margin" in request.form.keys():
        user_settings.algo_allow_margin = True
    else:
        user_settings.algo_allow_margin =False

    if "algo_apply_min_rank" in request.form.keys():
        user_settings.algo_apply_min_rank = True
    else:
        user_settings.algo_apply_min_rank =False
    user_settings.algo_min_rank = request.form['algo_min_rank']

    user_settings.connection_port = request.form['connection_port']
    user_settings.connection_account_name = request.form['connection_account_name']
    user_settings.connection_tws_user = request.form['connection_tws_user']
    user_settings.connection_tws_pass = request.form['connection_tws_pass']
    user_settings.server_url = request.form['server_url']
    user_settings.server_report_interval_sec = request.form['server_report_interval_sec']

    if "server_use_system_candidates" in request.form.keys():
        user_settings.server_use_system_candidates = True
    else:
        user_settings.server_use_system_candidates = False
    user_settings.station_interval_worker_sec = request.form['station_interval_worker_sec']
    user_settings.station_interval_ui_sec = request.form['station_interval_ui_sec']

    user_settings.update_user_settings()
    return redirect(url_for('algotradersettings.usersettings'))

@csrf.exempt
@algotradersettings.route('/retrieveusersettings', methods=['GET'])
def retrieve_user_settings():
    request_data = request.get_json()
    logged_user = request_data["user"]

    user_settings = UserSetting.query.filter_by(email=logged_user).first()
    tdj=json.dumps(user_settings.toDictionary())
    parsed_response = json.dumps(tdj)
    return parsed_response
