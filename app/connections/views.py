from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from datetime import datetime
from app import db, csrf
from app.models import User,Connection

connections = Blueprint('connections', __name__)


@csrf.exempt
@connections.route('/logconnection', methods=['POST'])
def logconnection():
    request_data = request.get_json()
    logged_user = request_data["user"]
    users = User.query.all()
    if any(x.email == logged_user for x in users):
        c=Connection()
        c.email=logged_user
        now = datetime.now()
        c.reported_connection=now
        c.log_connection()
        return "Application launch for " + logged_user + " is logged."
    else:
        return "The user configured is not found on Server the connection is not logged"
