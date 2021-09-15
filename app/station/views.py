import fileinput
from shutil import copyfile

from flask import (
    Blueprint,
    render_template,
    send_from_directory
)
from flask_login import current_user

from app.models import UserSetting
import os
from pathlib import Path

station = Blueprint('station', __name__)


@station.route('/requirements', methods=['GET'])
def download():
    contract_txt = ''
    if not current_user.signature:
        try:
            # f = open('app/static/files/contract_ru.txt', encoding="utf8")
            # file_contents = f.read()
            # print(file_contents)
            # f.close()
            with open('app/static/files/contract_ru.txt', encoding="utf8") as f:
                contract_txt = f.read()
        except Exception as e:
            print(e)
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()
    return render_template('userview/download.html', user=current_user, user_settings=user_settings, contract_txt=contract_txt)


def create_script_for_package():
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()

    if user_settings is not None:
        # windows
        origin = './app/static/installation_templates/win_twsRestartScript_template.vbs'
        destination = './app/static/algotrader-station/algotrader/Scripts/win_twsRestartScript.vbs'
        copyfile(origin, destination)
        with fileinput.FileInput(destination, inplace=True) as file:
            for line in file:
                print(line.replace("tws_user", user_settings.connection_tws_user), end='')
        with fileinput.FileInput(destination, inplace=True) as file:
            for line in file:
                print(line.replace("tws_password", user_settings.connection_tws_pass), end='')
        # linux
        origin = './app/static/installation_templates/tws_cred_login_template.py'
        destination = './app/static/algotrader-station/algotrader/Scripts/tws_cred_login.py'
        copyfile(origin, destination)
        with fileinput.FileInput(destination, inplace=True) as file:
            for line in file:
                print(line.replace("tws_user", user_settings.connection_tws_user), end='')
        with fileinput.FileInput(destination, inplace=True) as file:
            for line in file:
                print(line.replace("tws_password", user_settings.connection_tws_pass), end='')


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
        shutil.rmtree('./app/static/ready_package/algotrader' + uid + '.zip')  # removing prev packages
    except:
        pass
    # create_script_for_package()
    create_config_for_package()
    shutil.make_archive('./app/static/ready_package/algotrader' + uid, 'zip', 'app/static', 'algotrader-station')

    return send_from_directory(
        directory='static/ready_package',
        filename='algotrader' + uid + '.zip'
    )


@station.route('/download_contract', methods=['GET'])
def download_contract():
    return send_from_directory(
        directory='static/files',
        filename='contract_ru.pdf'
    )
