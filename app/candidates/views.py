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

@candidates.route('add_by_spider', methods=['POST'])
@csrf.exempt
def add_by_spider():
    ticker_to_add= request.form['ticker_to_add']
    company_name= request.form['company_name']
    sector= request.form['sector']
    p_e= request.form['p_e']

    c=Candidate()
    c.ticker=ticker_to_add
    c.reason="Added by spider"
    c.company_name = company_name
    c.full_description = "Spider does not have it"
    c.exchange = "Spider does not have it"
    c.industry = sector
    c.logo = "Spider does not have it"
    c.email='admin@gmail.com'
    c.enabled=True
    candidate = Candidate.query.filter((Candidate.email == 'admin@gmail.com') & (Candidate.ticker == ticker_to_add)).first()
    if candidate is None:
        db.session.add(c)
        db.session.commit()
        research_ticker(c.ticker)

    return "successfully added candidate"

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
@candidates.route('/info', methods=['GET'])
def info():

    ticker=request.args['ticker_to_show']
    candidate = Candidate.query.filter_by(ticker=ticker).first()
    m_data=TickerData.query.filter_by(ticker=ticker).order_by(TickerData.updated_server_time.desc()).first()
    user_settings = UserSetting.query.filter_by(email=current_user.email).first()
    td_history = TickerData.query.filter_by(ticker=ticker).order_by(TickerData.updated_server_time.asc()).all()
    hist_dates=[]
    hist_tr_ranks=[]
    hist_fmp_score=[]
    for td in td_history:
        hist_dates.append(td.updated_server_time.strftime("%m/%d/%Y"))
        hist_tr_ranks.append(td.tipranks)
        hist_fmp_score.append(td.fmp_score)
        t=2



    return render_template('candidates/ticker_info.html',user_settings=user_settings,
                           candidate=candidate,
                           market_data=m_data,
                           hist_dates=hist_dates,
                           hist_tr_ranks=hist_tr_ranks,
                           hist_fmp_score=hist_fmp_score)
