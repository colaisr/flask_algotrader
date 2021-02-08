from flask import Blueprint, render_template

from app.models import EditableHTML, Connection

main = Blueprint('main', __name__)


@main.route('/')
def index():
    last_connections = Connection.query.order_by(Connection.reported_connection.desc()).limit(10).all()
    return render_template('main/index.html', connections=last_connections)


@main.route('/about')
def about():
    editable_html_obj = EditableHTML.get_editable_html('about')
    return render_template(
        'main/about.html', editable_html_obj=editable_html_obj)
