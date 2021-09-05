import requests


def get_stock_invest_rank_for_ticker(ticker):
    score = 0
    try:
        url = "https://stockinvest.us/stock/" + ticker
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }
        r = requests.get(url, headers=headers)
        if not r.ok:
            score = 0
        try:
            response_text = r.text
            sentence_starts = response_text.find('Current score')
            left_part = response_text.find('>', sentence_starts)
            righ_part = response_text.find('<', left_part)
            score = response_text[left_part + 1:righ_part]
            score = float(score)
        except:
            score = 0
    except:
        score = 0
    return score


if __name__ == '__main__':
    s = get_stock_invest_rank_for_ticker('bkh')
