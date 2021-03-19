import requests
def get_tiprank_for_ticker(ticker):
    url = "https://www.tipranks.com/api/stocks/stockAnalysisOverview/?tickers=" + ticker

    url = requests.get(url)
    result=url.json()
    score=result[0]['smartScore']
    return score