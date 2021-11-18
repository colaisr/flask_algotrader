import ssl
import json
import certifi

from flask import (
    Blueprint,
    render_template,
    jsonify,
    request
)
from app import csrf, env
from urllib.request import urlopen


api = Blueprint('api', __name__)
spyder_url = 'http://localhost:8000' if env == 'DEV' else 'https://colak.eu.pythonanywhere.com'


@api.route('/stock_news', methods=['GET'])
@csrf.exempt
def stock_news():
    tickers = request.args.get('tickers')
    limit = request.args.get('limit')
    url = (
            f"{spyder_url}/data_hub/stock_news?tickers={tickers}&limit={limit}")
    data = api_request(url)
    return jsonify({'data': render_template('partial/ticket_info_news.html', data=json.loads(data))})


@api.route('/insider_actions', methods=['GET'])
@csrf.exempt
def insider_actions():
    ticker = request.args.get('ticker')
    url = (
            f"{spyder_url}/data_hub/insider_actions/{ticker}")
    data = api_request(url)
    return jsonify({'data': render_template('partial/ticket_info_insiders.html', data=json.loads(data))})


def api_request(url):
    context = ssl.create_default_context(cafile=certifi.where())
    response = urlopen(url, context=context)
    return response.read().decode("utf-8")