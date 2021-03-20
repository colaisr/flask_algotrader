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
from app.models import User, Connection, Report, TickerData, Candidate

candidates = Blueprint('candidates', __name__)

@candidates.route('usercandidates', methods=['GET', 'POST'])
@login_required
def usercandidates():
    candidates=Candidate.query.filter_by(email=current_user.email).all()
    return render_template('candidates/usercandidates.html',candidates=candidates, user=current_user, form=None)

@candidates.route('updatecandidate/', methods=['POST'])
@csrf.exempt
def updatecandidate():

    c=Candidate()
    c.ticker=request.form['txt_ticker']
    c.description=request.form['txt_description']
    c.email=current_user.email
    c.update_candidate()
    c.enabled=True
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
    use_system_candidates=request_data["use_system_candidates"]
    logged_user = request_data["user"]
    user_candidates=Candidate.query.filter_by(email=logged_user,enabled=True).all()
    if use_system_candidates:
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