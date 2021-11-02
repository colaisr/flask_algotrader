from flask import Blueprint, render_template, url_for
from flask_login import current_user
from sqlalchemy import text
from werkzeug.utils import redirect

import app.generalutils as general
import app.enums as enum

from app.models import EditableHTML, User, TickerData, Position, Report, LastUpdateSpyderData

from app import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.users_monitor'))
        if current_user.subscription_type_id == enum.Subscriptions.PERSONAL.value:
            return redirect(url_for('candidates.today'))
        elif current_user.subscription_type_id == enum.Subscriptions.MANAGED_PORTFOLIO.value:
            return redirect(url_for('userview.traderstationstate'))

    system_status = {}
    query_text = "select a.* from Tickersdata a join (  select Tickersdata.`ticker`, max(Tickersdata.`updated_server_time`) as updated_server_time  from Tickersdata group by Tickersdata.`ticker`) b on b.`ticker`=a.`ticker` and b.`updated_server_time`=a.`updated_server_time`"
    uniq_tickers_data = db.session.query(TickerData).from_statement(text(query_text)).all()
    system_status['tickers_tracked'] = len(uniq_tickers_data)

    last_update_date = db.session.query(LastUpdateSpyderData.last_update_date).order_by(LastUpdateSpyderData.start_process_time.desc()).first().last_update_date
    central = general.utc_datetime_to_local(last_update_date)
    system_status['last_update_date'] = central.strftime("%d %b, %Y")

    all_users = User.query.all()
    personal_users = list(filter(lambda p: p.subscription_type_id == enum.Subscriptions.PERSONAL.value, all_users))
    managed_users = list(filter(lambda p: p.subscription_type_id == enum.Subscriptions.MANAGED_PORTFOLIO.value, all_users))
    system_status['users_registered'] = len(all_users)
    system_status['personal_users'] = len(personal_users)
    system_status['managed_users'] = len(managed_users)

    closed_positions = Position.query.filter(Position.last_exec_side == 'SLD').all()
    lost_positions = list(filter(lambda p: p.profit <= 0 and (p.profit / (p.open_price * p.stocks) * 100) < -9, closed_positions))
    profit_positions = list(filter(lambda p: p.profit > 0 and (p.profit / (p.open_price * p.stocks) * 100) >= 5, closed_positions))
    technical_positions = list(filter(lambda p: (p.profit > 0 and (p.profit / (p.open_price * p.stocks) * 100) < 5) or (p.profit <= 0 and (p.profit / (p.open_price * p.stocks) * 100) >= -9), closed_positions))
    system_status['lost_positions'] = len(lost_positions)
    system_status['profit_positions'] = len(profit_positions)
    system_status['technical_positions'] = len(technical_positions)
    system_status['all_positions'] = len(closed_positions)
    system_status['funds'] = db.session.query(db.func.sum(Report.net_liquidation)).scalar()
    # return render_template('main/index_old.html', system_status=system_status)
    return render_template('main/index.html', system_status=system_status)


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)
