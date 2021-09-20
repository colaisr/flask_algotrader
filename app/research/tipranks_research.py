import requests


def get_tiprank_for_ticker(ticker):
    score = 0
    try:
        url = "https://www.tipranks.com/api/stocks/stockAnalysisOverview/?tickers=" + ticker

        url = requests.get(url)
        result = url.json()
        score = result[0]['smartScore']
        momentum = result[0]['technicalsTwelveMonthsMomentum']
        if score is None:
            score = 0
        if momentum is None:
            momentum = 0
    except:
        score = 0
        momentum = 0
    return score, momentum


if __name__ == '__main__':
    r, q = get_tiprank_for_ticker('ABCL')
