from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from app import db
from app.models import User
connections = Blueprint('connections', __name__)

@connections.route('/logconnection', methods=['GET', 'POST'])
def logconnection():
    i=2