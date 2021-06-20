import fileinput
import io
import os
import pathlib
import zipfile
from shutil import copyfile

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for, jsonify, send_file, app, send_from_directory,
)
from flask_login import current_user

from app.models import UserSetting

station=Blueprint('station', __name__)

@station.route('/download', methods=['GET'])
def download():
    uemail=current_user.email
    return render_template('userview/download.html', user=current_user)


def create_script_for_package():
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()

    if user_settings is not None:
        #windows
        origin='./app/static/installation_templates/win_twsRestartScript_template.vbs'
        destination = './app/static/algotrader-station/algotrader/Scripts/win_twsRestartScript.vbs'
        copyfile(origin, destination)
        with fileinput.FileInput(destination, inplace=True) as file:
            for line in file:
                print(line.replace("tws_user", user_settings.connection_tws_user), end='')
        with fileinput.FileInput(destination, inplace=True) as file:
            for line in file:
                print(line.replace("tws_password", user_settings.connection_tws_pass), end='')
        #linux
        # origin = './app/static/installation_templates/linux_twsRestartScript_template.sh'
        # destination = './app/static/algotrader-station/algotrader/Scripts/linux_twsRestartScript.sh'
        # copyfile(origin, destination)
        # with fileinput.FileInput(destination, inplace=True) as file:
        #     for line in file:
        #         print(line.replace("tws_user", user_settings.connection_tws_user), end='')
        # with fileinput.FileInput(destination, inplace=True) as file:
        #     for line in file:
        #         print(line.replace("tws_password", user_settings.connection_tws_pass), end='')


def create_config_for_package():
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()

    if user_settings is not None:
        origin = './app/static/installation_templates/config_template.ini'
        destination = './app/static/algotrader-station/algotrader/config.ini'
        copyfile(origin, destination)
        with fileinput.FileInput(destination, inplace=True) as file:
            for line in file:
                print(line.replace("server_user", user_settings.email), end='')


@station.route('/downloadzip', methods=['GET'])
def request_zip():
    import shutil
    uid = str(current_user.id)
    try:
        shutil.rmtree('./app/static/ready_package/algotrader'+uid+'.zip') #removing prev packages
    except:
        i=2
    create_script_for_package()
    create_config_for_package()
    shutil.make_archive('./app/static/ready_package/algotrader'+uid, 'zip', 'app/static','algotrader-station')

    return send_from_directory(
        directory='static/ready_package',
        filename='algotrader'+uid+'.zip'
    )
