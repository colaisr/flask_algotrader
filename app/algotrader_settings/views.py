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
