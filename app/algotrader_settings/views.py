import json

import jsonpickle
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for, jsonify,
)
from datetime import datetime, date, timedelta

from flask_login import login_required, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.ext.sqlalchemy.orm import model_form
from wtforms.validators import DataRequired

from app import db, csrf
from app.models import User, Connection, Report, TickerData, UserSetting

algotradersettings = Blueprint('algotradersettings', __name__)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


class Settings_form(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    account = StringField('Account', validators=[DataRequired()])
    submit = SubmitField('Save')

@algotradersettings.route('/usersettings', methods=['GET','POST'])
@login_required
def usersettings():
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()

    if user_settings is None:      #default settings for user
        user_settings=UserSetting()
        user_settings.email=current_user.email

        user_settings.algo_max_loss=10
        user_settings.algo_take_profit=6
        user_settings.algo_bulk_amount_usd=1000
        user_settings.algo_trailing_percent=1

        user_settings.connection_account_name = 'Default,needs to be changed'
        user_settings.connection_port=7498
        user_settings.connection_break_from_hour=8
        user_settings.connection_break_from_min=0
        user_settings.connection_break_to_hour=8
        user_settings.connection_break_to_min=1

        user_settings.station_debug_ui=True
        user_settings.station_autostart_worker=True
        user_settings.station_interval_ui_sec=1
        user_settings.station_interval_worker_sec=60
        user_settings.station_mac_path_to_webdriver='Research/chromedriverM'
        user_settings.station_win_path_to_webdriver = 'Research/chromedriverW.exe'
        user_settings.station_linux_path_to_webdriver = 'Research/chromedriverl'

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
