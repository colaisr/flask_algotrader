from flask import Blueprint, render_template, url_for, request
from flask_login import current_user
from sqlalchemy import text
from werkzeug.utils import redirect

import app.generalutils as general
import app.enums as enum

from app.models import EditableHTML, User, Candidate, Position, Report, LastUpdateSpyderData

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
    query_text = "SELECT * FROM Candidates WHERE enabled=1 GROUP BY ticker"
    uniq_tickers_data = db.session.query(Candidate).from_statement(text(query_text)).all()
    system_status['tickers_tracked'] = len(uniq_tickers_data)

    last_update_date = db.session.query(LastUpdateSpyderData.last_update_date).order_by(LastUpdateSpyderData.start_process_time.desc()).first().last_update_date
    central = general.utc_datetime_to_local(last_update_date)
    system_status['last_update_date'] = central.strftime("%d %b, %Y")

    all_users = User.query.filter(User.role_id == enum.UserRole.USER.value).all()
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
    return render_template('mainpage/main.html', system_status=system_status)


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)
