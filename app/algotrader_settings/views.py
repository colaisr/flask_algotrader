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
from wtforms.validators import DataRequired

from app import db, csrf
from app.models import User, Connection, Report, TickerData

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
    form = Settings_form()

    if form.validate_on_submit():
        name=form.username.data
        account=form.account.data
    else:
        form.username.data = 'default Name'
        form.account.data = 'default Account'

    return render_template('userview/algotraderSettings.html',user=current_user, form=form)


