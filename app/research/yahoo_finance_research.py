import requests
def get_yahoo_rank_for_ticker(ticker):
    score=0
    try:
        lhs_url = 'https://query2.finance.yahoo.com/v10/finance/quoteSummary/'
        rhs_url = '?formatted=true&crumb=swg7qs5y9UP&lang=en-US&region=US&' \
                  'modules=upgradeDowngradeHistory,recommendationTrend,' \
                  'financialData,earningsHistory,earningsTrend,industryTrend&' \
                  'corsDomain=finance.yahoo.com'

        url = lhs_url + ticker + rhs_url
        headers = {
            'User-Agent': ''

        }
        r = requests.get(url,headers=headers)
        if not r.ok:
            recommendation = 6
        try:
            result = r.json()['quoteSummary']['result'][0]
            recommendation = result['financialData']['recommendationMean']['fmt']
        except:
            recommendation = 6
    except:
        score=6
    return float(recommendation)

if __name__ == '__main__':
    get_yahoo_rank_for_ticker('MSFT')