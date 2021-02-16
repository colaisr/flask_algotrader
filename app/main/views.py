from flask import Blueprint, render_template, url_for
from flask_login import current_user
from werkzeug.utils import redirect

from app.models import EditableHTML, Connection

main = Blueprint('main', __name__)


@main.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('userview.traderstationstate'))
    else:
        last_connections = Connection.query.order_by(Connection.reported_connection.desc()).limit(10).all()
        return render_template('main/index.html', connections=last_connections)


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)
