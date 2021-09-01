import json
from flask import (
    Blueprint,
    flash,
    render_template,
    request, url_for
)
from datetime import datetime, date

from flask_login import login_required, current_user

from werkzeug.utils import redirect

from app import csrf
from app.models import UserSetting, Strategy, UserStrategySettingsDefault
from app.email import send_email

algotradersettings = Blueprint('algotradersettings', __name__)


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


# @algotradersettings.route('/usersettings/', defaults={'strategy_id': None}, methods=['GET', 'POST'])
@algotradersettings.route('/usersettings/', methods=['GET'])
@login_required
def usersettings():
    if not current_user.admin_confirmed:
        return redirect(url_for('station.download'))
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()
    # if strategy_id is not None:
    #     default_settings = UserStrategySettingsDefault.query.filter_by(id=strategy_id).first()
    # else:
    #     default_settings = UserStrategySettingsDefault(
    #         strategy_id=user_settings.strategy_id,
    #         algo_min_rank=user_settings.algo_min_rank,
    #         algo_accepted_fmp_ratings=user_settings.algo_accepted_fmp_ratings,
    #         algo_max_yahoo_rank=user_settings.algo_max_yahoo_rank,
    #         algo_min_stock_invest_rank=user_settings.algo_min_stock_invest_rank,
    #         algo_min_underprice=user_settings.algo_min_underprice,
    #         algo_min_momentum=user_settings.algo_min_momentum,
    #         algo_apply_min_rank=user_settings.algo_apply_min_rank,
    #         algo_apply_accepted_fmp_ratings=user_settings.algo_apply_accepted_fmp_ratings,
    #         algo_apply_max_yahoo_rank=user_settings.algo_apply_max_yahoo_rank,
    #         algo_apply_min_stock_invest_rank=user_settings.algo_apply_min_stock_invest_rank,
    #         algo_apply_min_underprice=user_settings.algo_apply_min_underprice,
    #         algo_apply_min_momentum=user_settings.algo_apply_min_momentum
    #     )

    # strategies = Strategy.query.filter(Strategy.id != 4).all()
    return render_template('userview/algotraderSettings.html',
                           user_settings=user_settings)
                           # strategies=strategies,
                           # default_settings=default_settings)


@algotradersettings.route('/savesettings', methods=['POST'])
@login_required
def savesettings():
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()
    user_settings.algo_max_loss = request.form['algo_max_loss']
    user_settings.algo_take_profit = request.form['algo_take_profit']
    user_settings.algo_bulk_amount_usd = request.form['algo_bulk_amount_usd']
    user_settings.algo_trailing_percent = request.form['algo_trailing_percent']
    if "algo_apply_accepted_fmp_ratings" in request.form.keys():
        user_settings.algo_apply_accepted_fmp_ratings = True
    else:
        user_settings.algo_apply_accepted_fmp_ratings = False
    user_settings.algo_accepted_fmp_ratings = request.form['algo_accepted_fmp_ratings']

    if "algo_apply_max_yahoo_rank" in request.form.keys():
        user_settings.algo_apply_max_yahoo_rank = True
    else:
        user_settings.algo_apply_max_yahoo_rank = False
    user_settings.algo_max_yahoo_rank = request.form['algo_max_yahoo_rank']

    if "algo_apply_max_hold" in request.form.keys():
        user_settings.algo_apply_max_hold = True
    else:
        user_settings.algo_apply_max_hold = False
    user_settings.algo_max_hold_days = request.form['algo_max_hold_days']

    if "algo_allow_buy" in request.form.keys():
        user_settings.algo_allow_buy = True
    else:
        user_settings.algo_allow_buy = False

    if "algo_allow_sell" in request.form.keys():
        user_settings.algo_allow_sell = True
    else:
        user_settings.algo_allow_sell = False

    if "algo_allow_margin" in request.form.keys():
        user_settings.algo_allow_margin = True
    else:
        user_settings.algo_allow_margin = False

    if "station_autorestart" in request.form.keys():
        user_settings.station_autorestart = True
    else:
        user_settings.station_autorestart = False

    if "algo_apply_min_rank" in request.form.keys():
        user_settings.algo_apply_min_rank = True
    else:
        user_settings.algo_apply_min_rank = False
    user_settings.algo_min_rank = request.form['algo_min_rank']

    if "algo_sell_on_swan" in request.form.keys():
        user_settings.algo_sell_on_swan = True
    else:
        user_settings.algo_sell_on_swan = False
    user_settings.algo_positions_for_swan = request.form['algo_positions_for_swan']

    if "notify_buy" in request.form.keys():
        user_settings.notify_buy = True
    else:
        user_settings.notify_buy = False

    if "notify_sell" in request.form.keys():
        user_settings.notify_sell = True
    else:
        user_settings.notify_sell = False

    if "notify_trail" in request.form.keys():
        user_settings.notify_trail = True
    else:
        user_settings.notify_trail = False

    if "algo_apply_min_underprice" in request.form.keys():
        user_settings.algo_apply_min_underprice = True
    else:
        user_settings.algo_apply_min_underprice = False
    user_settings.algo_min_underprice = request.form['algo_min_underprice']

    if "algo_apply_min_momentum" in request.form.keys():
        user_settings.algo_apply_min_momentum = True
    else:
        user_settings.algo_apply_min_momentum = False
    user_settings.algo_min_momentum = request.form['algo_min_momentum']

    if "algo_apply_min_stock_invest_rank" in request.form.keys():
        user_settings.algo_apply_min_stock_invest_rank = True
    else:
        user_settings.algo_apply_min_stock_invest_rank = False
    user_settings.algo_min_stock_invest_rank = request.form['algo_min_stock_invest_rank']

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

    # user_settings.strategy_id = request.form['strategy_id']

    user_settings.update_user_settings()
    return redirect(url_for('algotradersettings.usersettings'))


@algotradersettings.route('/saverequirementssettings', methods=['POST'])
@login_required
def saverequirementssettings():
    connection_account_name = request.form['connection_account_name']
    connection_tws_user = request.form['connection_tws_user']
    connection_tws_pass = request.form['connection_tws_pass']

    if connection_account_name == 'U0000000' \
            or connection_tws_user == 'your_tws_user_name' \
            or connection_tws_pass == 'your_tws_user_password':
        flash('Validate credentials', 'error')
    else:
        user_settings = UserSetting.query.filter_by(email=current_user.email).first()
        user_settings.connection_account_name = connection_account_name
        user_settings.connection_tws_user = connection_tws_user
        user_settings.connection_tws_pass = connection_tws_pass

        user_settings.update_user_settings()
        flash('Credentials saved', 'success')

        current_user.tws_requirements = 1
        current_user.update_user()

        url = url_for('admin.pending_approval', _external=True)

        send_email(recipient='support@algotrader.company',
                   subject='Algotrader Server: user provided all the details',
                   template='account/email/user_data_provided',
                   user=current_user,
                   url=url)

    return redirect(url_for('station.download'))


@csrf.exempt
@algotradersettings.route('/retrieveusersettings', methods=['GET'])
def retrieve_user_settings():
    request_data = request.get_json()
    logged_user = request_data["user"]

    user_settings = UserSetting.query.filter_by(email=logged_user).first()
    tdj = json.dumps(user_settings.toDictionary())
    parsed_response = json.dumps(tdj)
    return parsed_response
