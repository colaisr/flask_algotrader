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

@station.route('/download-zip', methods=['GET'])
def request_zip():
    import shutil
    # base_path = pathlib.Path('./app/static/algotrader-station/')
    # h = pathlib.Path.cwd()
    # p=pathlib.Path.joinpath(h,'/app/')
    shutil.make_archive('exampleOrg_letter', 'zip', './app/static/algotrader-station/','./app/static/algotrader-station/')
    #
    # data = io.BytesIO()
    # with zipfile.ZipFile(data, mode='w') as z:
    #     for f_name in base_path.iterdir():
    #         z.write(f_name)
    # data.seek(0)
    h = pathlib.Path.cwd()
    p=pathlib.Path.joinpath(h,'/static/test.zip')
    return send_from_directory(
        directory='static',
        filename='test.zip'
    )