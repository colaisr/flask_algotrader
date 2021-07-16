import requests
def get_tiprank_for_ticker(ticker):
    score=0
    try:
        url = "https://www.tipranks.com/api/stocks/stockAnalysisOverview/?tickers=" + ticker

        url = requests.get(url)
        result=url.json()
        score=result[0]['smartScore']
        if score is None:
            score=0
    except:
        score=0
    return score