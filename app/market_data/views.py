import json

import jsonpickle
from flask import (
    Blueprint,
    flash,
    redirect,
    render_template,
    request,
    url_for, jsonify,
)
from datetime import datetime, date, timedelta
from app import db, csrf
from app.models import User, Connection, Report, TickerData

marketdata = Blueprint('marketdata', __name__)

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))



@csrf.exempt
@marketdata.route('/updatemarketdata', methods=['POST'])
def updatemarketdata():
    request_data = request.get_json()
    received_data=request_data["tickers"]
    logged_user = request_data["user"]
    parsed_data = json.loads(received_data)
    for marker in parsed_data:
        s=marker['ticker']
        d=marker['yahoo_avdropP']
        sp=marker['yahoo_avspreadP']
        r=marker['tipranks']
        u=datetime.fromisoformat(marker['updated'])
        t=TickerData(ticker=s,yahoo_avdropP=d,yahoo_avspreadP=sp,tipranks=r,updated=u)
        if int(t.tipranks)!=0:
            t.update_ticker_data()

    return "Market data updated at server"
@csrf.exempt
@marketdata.route('/retrievemarketdata', methods=['GET'])
def retrievemarketdata():
    request_data = request.get_json()
    received_data=request_data["tickers"]
    logged_user = request_data["user"]
    parsed_data = json.loads(received_data)
    requested_tickers={}
    for t in parsed_data:
        td=TickerData.query.filter_by(ticker=t).first()

        if td is None:#not data-fake
            td=TickerData(ticker=t,yahoo_avdropP=0,yahoo_avspreadP=0,tipranks=0,updated=(datetime.today() - timedelta(days=1)))

        tdj=json.dumps(td.toDictionary())



        requested_tickers[td.ticker]=tdj
    parsed_response=json.dumps(requested_tickers)




    return requested_tickers

# @csrf.exempt
# @marketdata.route('/postreport', methods=['POST'])
# def logreport():
#     request_data = request.get_json()
#     logged_user = request_data["user"]
#     users = User.query.all()
#     if any(x.email == logged_user for x in users):
#         report = Report.query.filter_by(email=logged_user).first()
#         if report is None:
#             report = Report()
#         report.email = logged_user
#         now = datetime.now()
#         report.report_time = now
#         report.remaining_trades = request_data["remaining_trades"]
#         report.open_positions_json = request_data["open_positions"]
#         report.open_orders_json = request_data["open_orders"]
#         report.all_positions_value = request_data["all_positions_value"]
#         report.net_liquidation = request_data["net_liquidation"]
#         report.remaining_sma_with_safety = request_data["remaining_sma_with_safety"]
#         report.dailyPnl = request_data["dailyPnl"]
#         report.log_report()
#
#
#         return "Report for " + logged_user + " stored at server."
#     else:
#         return "The user configured is not found on Server the report is not logged"
