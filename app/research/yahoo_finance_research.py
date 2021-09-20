import requests


def get_yahoo_rank_for_ticker(ticker):
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
        r = requests.get(url, headers=headers)
        if not r.ok:
            recommendation = 6
        try:
            result = r.json()['quoteSummary']['result'][0]
            recommendation = result['financialData']['recommendationMean']['raw']

            targetMeanPrice = result['financialData']['targetMeanPrice']['raw']
            current_price = result['financialData']['currentPrice']['raw']
            difference = targetMeanPrice - current_price
            under_priced_percents = round(difference / targetMeanPrice * 100, 1)
        except:
            recommendation = 6
            under_priced_percents = 0
            targetMeanPrice = 0
    except:
        recommendation = 6
        under_priced_percents = 0
        targetMeanPrice=0
    return recommendation, under_priced_percents,targetMeanPrice


if __name__ == '__main__':
    get_yahoo_rank_for_ticker('abcl')
