import json
import ssl
import app.generalutils as general
from urllib.request import urlopen

from flask import (
    Blueprint,
    render_template,
    request
)
from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from app import csrf
from app.models import TickerData, Position, ReportStatistic

closed_position_info = Blueprint('closed_position_info', __name__)
apikey = 'f6003a61d13c32709e458a1e6c7df0b0'


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def get_fmg_pe_rating_for_ticker(s):
    # data=fmpsdk.financial_ratios(apikey=apikey, symbol=s)
    url = ("https://financialmodelingprep.com/api/v3/ratios-ttm/" + s + "?apikey=" + apikey)
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    parsed = json.loads(data)
    pe = parsed[0]['peRatioTTM']
    url = ("https://financialmodelingprep.com/api/v3/rating/" + s + "?apikey=" + apikey)
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    parsed = json.loads(data)
    rating = parsed[0]['rating']
    score = parsed[0]['ratingScore']

    return pe, rating, score


@csrf.exempt
@closed_position_info.route('/view', methods=['GET'])
def view():
    id = request.args['position_to_show']
    position = Position.query.filter_by(id=id).first()
    hist = TickerData.query.filter_by(ticker=position.ticker).order_by(TickerData.updated_server_time.asc()).all()
    rank_array = []
    for h in hist:
        rank_array.append([str(h.updated_server_time.strftime("%d %b, %Y %H:%M:%S")), h.tipranks])
    return render_template('userview/closed_position_info.html', position=position, rank_array=rank_array)


@csrf.exempt
@closed_position_info.route('/user_reports_history', methods=['POST'])
def user_reports_history():
    user = request.form.get('user')
    from_date_str = request.form.get('from_date')
    to_date_str = request.form['to_date']
    from_date = datetime.strptime(from_date_str.split(' GMT')[0], '%a %b %d %Y %X')
    to_date = datetime.strptime(to_date_str.split(' GMT')[0], '%a %b %d %Y %X') + relativedelta(days=1)
    history = ReportStatistic.query.filter(ReportStatistic.email == user,
                                           ReportStatistic.report_time.between(from_date, to_date)).all()
    return json.dumps(history, cls=general.JsonEncoder)
