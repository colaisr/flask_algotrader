import app.generalutils as general
import json
import app.api_service.api_mapping as map
from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    redirect,
    url_for
)
from app import csrf, env


api = Blueprint('api', __name__)
spyder_url = 'http://localhost:8000' if env == 'DEV' else 'https://colak.eu.pythonanywhere.com'
# spyder_url = 'https://colak.eu.pythonanywhere.com'


@api.route('/stock_news', methods=['GET'])
@csrf.exempt
def stock_news():
    tickers = request.args.get('tickers')
    limit = request.args.get('limit')
    url = (
            f"{spyder_url}/data_hub/stock_news?tickers={tickers}&limit={limit}")
    data = general.api_request_get(url)
    return jsonify({'data': render_template('partial/ticket_info_news.html', data=json.loads(data))})


@api.route('/insider_actions', methods=['GET'])
@csrf.exempt
def insider_actions():
    ticker = request.args.get('ticker')
    url = (
            f"{spyder_url}/data_hub/insider_actions/{ticker}")
    data = general.api_request_get(url)
    return jsonify({'data': render_template('partial/ticket_info_insiders.html', data=json.loads(data))})


@api.route('/press_relises', methods=['GET'])
@csrf.exempt
def press_relises():
    ticker = request.args.get('ticker')
    url = (
            f"{spyder_url}/data_hub/press_relises/{ticker}")
    data = general.api_request_get(url)
    return jsonify({'data': render_template('partial/ticket_info_press_relises.html', data=json.loads(data))})


@api.route('/search', methods=['GET'])
@csrf.exempt
def search():
    query = request.args.get('query')
    url = (
            f"{spyder_url}/data_hub/search/{query}")
    data = general.api_request_get(url)
    return data


@api.route('/add_candidate')
@csrf.exempt
def add_candidate():
    ticker = request.args.get('ticker')
    url = (
        f"{spyder_url}/candidates/add_by_spider")
    result = general.api_request_post(url, {'ticker_to_add': ticker})
    # resultJSON = json.loads(result.decode("utf-8"))
    if b'success' not in result:
        return f"We have no data for {ticker}. If you think it should be added please contact support@algotrader.company"
    else:
        return redirect(url_for('candidates.info', ticker=ticker))


@api.route('/fundamentals_summary', methods=['GET'])
@csrf.exempt
def fundamentals_summary():
    ticker = request.args.get('ticker')
    url = (
            f"{spyder_url}/data_hub/financial_ttm/{ticker}")
    data = general.api_request_get(url)
    data_json = json.loads(data)
    property_list = map.financial_ttm_mapping(data_json[0])
    return jsonify({'data': render_template('partial/ticker_info_fundamentals.html', data=property_list)})





