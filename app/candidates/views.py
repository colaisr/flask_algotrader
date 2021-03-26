import json
import ssl
from urllib.request import urlopen

from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for, jsonify,
)
from datetime import datetime, date, timedelta

from flask_login import login_required, current_user

from app import db, csrf
from app.models import User, Connection, Report, TickerData, Candidate, UserSetting
from app.research.views import research_ticker

candidates = Blueprint('candidates', __name__)

@candidates.route('usercandidates', methods=['GET', 'POST'])
@login_required
def usercandidates():
    candidates=Candidate.query.filter_by(email=current_user.email).all()
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()
    admin_candidates={}
    if user_settings.server_use_system_candidates:
        admin_candidates = Candidate.query.filter_by(email='admin@gmail.com', enabled=True).all()
    return render_template('candidates/usercandidates.html',admin_candidates=admin_candidates,candidates=candidates, user=current_user, form=None)

@candidates.route('updatecandidate/', methods=['POST'])
@csrf.exempt
def updatecandidate():

    c=Candidate()
    c.ticker=request.form['txt_ticker']
    c.reason=request.form['txt_reason']
    c.company_name = request.form['txt_company_name']
    c.full_description = request.form['txt_company_description']
    c.exchange = request.form['txt_exchange']
    c.industry = request.form['txt_industry']
    c.logo = request.form['txt_logo']
    c.email=current_user.email
    c.enabled=True
    c.update_candidate()
    research_ticker(c.ticker)

    return redirect(url_for('candidates.usercandidates'))

@candidates.route('removecandidate/', methods=['POST'])
@csrf.exempt
def removecandidate():
    ticker=request.form['ticker_to_remove']
    candidate = Candidate.query.filter_by(email=current_user.email,ticker=ticker).first()
    candidate.delete_candidate()
    return redirect(url_for('candidates.usercandidates'))

@candidates.route('enabledisable/', methods=['POST'])
@csrf.exempt
def enabledisable():
    ticker=request.form['ticker_to_change']
    candidate = Candidate.query.filter_by(email=current_user.email,ticker=ticker).first()
    candidate.change_enabled_state()
    return redirect(url_for('candidates.usercandidates'))

@csrf.exempt
@candidates.route('/retrieveusercandidates', methods=['GET'])
def retrievecandidates():
    request_data = request.get_json()
    logged_user = request_data["user"]
    user_candidates=Candidate.query.filter_by(email=logged_user,enabled=True).all()
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()

    if user_settings.server_use_system_candidates:
        admin_candidates=Candidate.query.filter_by(email='admin@gmail.com',enabled=True).all()
        for uc in user_candidates:
            for ac in admin_candidates:
                if ac.ticker == uc.ticker:
                    print("i found it!")
                    break
            else:
                admin_candidates.append(uc)
        requested_candidates=admin_candidates
    else:
        requested_candidates=user_candidates
    cand_dictionaries=[]
    for c in requested_candidates:
        cand_dictionaries.append(c.to_dictionary())
    response=json.dumps(cand_dictionaries)
    return response