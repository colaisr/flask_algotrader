from flask import Blueprint, render_template, url_for
from flask_login import current_user
from sqlalchemy import text
from werkzeug.utils import redirect

from app.models import EditableHTML, User, TickerData, Position

from app import db

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('userview.traderstationstate'))
    else:
        system_status={}
        system_status['users_count']=len(User.query.all())



        query_text = "select a.* from Tickersdata a join (  select Tickersdata.`ticker`, max(Tickersdata.`updated_server_time`) as updated_server_time  from Tickersdata group by Tickersdata.`ticker`) b on b.`ticker`=a.`ticker` and b.`updated_server_time`=a.`updated_server_time`"
        uniq_tickers_data = db.session.query(TickerData).from_statement(text(query_text)).all()
        system_status['tickers_tracked'] = len(uniq_tickers_data)

        last_candidate=TickerData.query.order_by(TickerData.id.desc()).first()
        last_update=last_candidate.updated_server_time
        system_status['last_candidates_update'] =last_update.strftime("%d-%b-%Y (%H:%M:%S)")
        system_status['users_registered'] = len(User.query.all())
        system_status['lost_positions'] = len(Position.query.filter(Position.profit <= 0).all())
        system_status['profit_positions'] = len(Position.query.filter(Position.profit >= 0).all())
        system_status['all_positions']=system_status['lost_positions']+ system_status['profit_positions']

        return render_template('main/index.html', system_status=system_status)


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)
