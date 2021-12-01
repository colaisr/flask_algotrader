import app.generalutils as general
from flask_login import current_user
from app.api_service import api_service
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
    data = api_service.stock_news_api(tickers, limit)
    return jsonify({'data': render_template('partial/ticket_info_news.html', data=data)})


@api.route('/insider_actions', methods=['GET'])
@csrf.exempt
def insider_actions():
    ticker = request.args.get('ticker')
    data = api_service.insider_actions_api(ticker)
    return jsonify({'data': render_template('partial/ticket_info_insiders.html', data=data)})


@api.route('/press_relises', methods=['GET'])
@csrf.exempt
def press_relises():
    ticker = request.args.get('ticker')
    data=api_service.press_relises_api(ticker)
    return jsonify({'data': render_template('partial/ticket_info_press_relises.html', data=data)})


@api.route('/search', methods=['GET'])
@csrf.exempt
def search():
    query = request.args.get('query')
    data = api_service.search_api(query)
    return data


@api.route('/search_quick', methods=['GET'])
@csrf.exempt
def search_quick():
    text_to_search = request.args.get('text_to_search')
    data = api_service.search_api(text_to_search)
    return data


@api.route('/add_candidate')
@csrf.exempt
def add_candidate():
    ticker = request.args.get('ticker')
    result = api_service.add_candidate_api(ticker)
    if result == 'success':
        return redirect(url_for('candidates.info', ticker=ticker))
    else:
        return result


@api.route('/add_favorite_candidate')
@csrf.exempt
def add_favorite_candidate():
    ticker = request.args.get('ticker')
    result = api_service.add_favorite_candidate_api(ticker, current_user.email)
    return result


@api.route('/fundamentals_summary', methods=['GET'])
@csrf.exempt
def fundamentals_summary():
    ticker = request.args.get('ticker')
    data = api_service.fundamentals_summary_api(ticker)
    property_list = map.financial_ttm_mapping(data[0])
    return jsonify({'data': render_template('partial/ticker_info_fundamentals.html', data=property_list)})


@api.route('/fundamentals_feed', methods=['GET'])
@csrf.exempt
def fundamentals_feed():
    ticker = request.args.get('ticker')
    data = api_service.fundamentals_feed_api(ticker)
    return jsonify({'data': render_template('partial/ticker_info_fundamentals_feed.html', data=data)})


@api.route('/company_info', methods=['GET'])
@csrf.exempt
def company_info():
    ticker = request.args.get('ticker')
    data = api_service.company_info_api(ticker)
    return jsonify({'data': render_template('partial/ticker_info_company_info.html', data=data)})


@api.route('/ticker_info/<ticker>', methods=['GET'])
@csrf.exempt
def ticker_info(ticker):
    data = api_service.company_info_api(ticker)
    return data





