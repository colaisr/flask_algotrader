import app.generalutils as general
import json

from app import env

spyder_url = 'http://localhost:8000' if env == 'DEV' else 'https://colak.eu.pythonanywhere.com'


def stock_news_api(tickers, limit):
    url = (
            f"{spyder_url}/data_hub/stock_news?tickers={tickers}&limit={limit}")
    data = general.api_request_get(url)
    return json.loads(data)


def insider_actions_api(ticker):
    url = (
            f"{spyder_url}/data_hub/insider_actions/{ticker}")
    data = general.api_request_get(url)
    return json.loads(data)


def press_relises_api(ticker):
    url = (
            f"{spyder_url}/data_hub/press_relises/{ticker}")
    data = general.api_request_get(url)
    return json.loads(data)


def add_candidate_api(ticker):
    url = (
        f"{spyder_url}/candidates/add_by_spider")
    result = general.api_request_post(url, {'ticker_to_add': ticker})
    # resultJSON = json.loads(result.decode("utf-8"))
    if b'success' not in result:
        return f"We have no data for {ticker}. If you think it should be added please contact support@stockscore.company"
    else:
        return "success"


def add_favorite_candidate_api(ticker, reason, email):
    url = (
        f"{spyder_url}/candidates/updatecandidate")
    result = general.api_request_post(url, {'ticker': ticker, 'reason': reason, 'email': email})
    resultJSON = json.loads(result.decode("utf-8"))
    if b'success' not in result:
        return f"We have no data for {ticker}. If you think it should be added please contact support@stockscore.company"
    else:
        return "success"


def fundamentals_summary_api(ticker):
    url = (
            f"{spyder_url}/data_hub/financial_ttm/{ticker}")
    data = general.api_request_get(url)
    return json.loads(data)


def fundamentals_feed_api(ticker):
    url = (
        f"{spyder_url}/data_hub/financial_statements/{ticker}")
    data = general.api_request_get(url)
    return json.loads(data)


def company_info_api(ticker):
    url = (
        f"{spyder_url}/research/get_info_ticker/{ticker}")
    data = general.api_request_get(url)
    return json.loads(data)


def search_quick(text_to_search):
    url = (
        f"{spyder_url}/data_hub/search_quick/{text_to_search}")
    data = general.api_request_get(url)
    return data


def search_api(query):
    url = (
            f"{spyder_url}/data_hub/search/{query}")
    data = general.api_request_get(url)
    return data

def similar_api(ticker):
    url = (
            f"{spyder_url}/data_hub/similar/{ticker}")
    data = general.api_request_get(url)
    return data