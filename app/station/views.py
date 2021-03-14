import io
import os
import pathlib
import zipfile

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for, jsonify, send_file, app, send_from_directory,
)
from flask_login import current_user

station=Blueprint('station', __name__)

@station.route('/download', methods=['GET'])
def download():
    uemail=current_user.email
    return render_template('userview/download.html', user=current_user)

@station.route('/downloadzip', methods=['GET'])
def request_zip():
    import shutil
    uid = str(current_user.id)
    try:
        shutil.rmtree('./app/static/ready_package/algotrader'+uid+'.zip') #removing prev packages
    except:
        i=2
    shutil.make_archive('./app/static/ready_package/algotrader'+uid, 'zip', 'app/static','algotrader-station')

    return send_from_directory(
        directory='static/ready_package',
        filename='algotrader'+uid+'.zip'
    )
