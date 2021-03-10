from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for, jsonify,
)
from flask_login import current_user

station=Blueprint('station', __name__)

@station.route('/download', methods=['GET'])
def download():
    uemail=current_user.email
    return render_template('userview/download.html', user=current_user)