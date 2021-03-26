import json
from flask import (
    Blueprint,
    render_template,
    request
)
from datetime import datetime, date, timedelta

from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms.ext.sqlalchemy.orm import model_form

from app import db, csrf
from app.models import UserSetting

algotradersettings = Blueprint('algotradersettings', __name__)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

@algotradersettings.route('/usersettings', methods=['GET','POST'])
@login_required
def usersettings():
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()

    if user_settings is None:      #default settings for user
        user_settings=UserSetting()
        user_settings.email=current_user.email

        user_settings.algo_max_loss=-10
        user_settings.algo_take_profit=6
        user_settings.algo_bulk_amount_usd=1000
        user_settings.algo_trailing_percent=1
        user_settings.algo_allow_buy=True
        user_settings.algo_allow_margin = True
        user_settings.algo_min_rank=8

        user_settings.connection_account_name = 'Default,needs to be changed'
        user_settings.connection_port=7498

        user_settings.station_interval_ui_sec=1
        user_settings.station_interval_worker_sec=60

        user_settings.server_url='http://colak.pythonanywhere.com'
        user_settings.server_report_interval_sec=30
        user_settings.server_use_system_candidates=True

    SettingsForm = model_form(UserSetting,base_class=FlaskForm)
    form=SettingsForm(obj=user_settings)
    if form.validate_on_submit():
        form.populate_obj(user_settings)
        user_settings.update_user_settings()
    return render_template('userview/algotraderSettings.html',user=current_user, form=form)

@csrf.exempt
@algotradersettings.route('/retrieveusersettings', methods=['GET'])
def retrieve_user_settings():
    request_data = request.get_json()
    logged_user = request_data["user"]

    user_settings = UserSetting.query.filter_by(email=logged_user).first()
    tdj=json.dumps(user_settings.toDictionary())
    parsed_response = json.dumps(tdj)
    return parsed_response
