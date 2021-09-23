import requests


def get_stock_invest_rank_for_ticker(ticker):
    score = 0
    print("***** Start stockinvest getting process")
    try:
        url = "https://stockinvest.us/stock/" + ticker
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }
        r = requests.get(url, headers=headers)
        print(f"r.ok: {r.ok}")
        if not r.ok:
            score = 0
        try:
            response_text = r.text
            # print(f"response_text: {response_text}")
            sentence_starts = response_text.find('Current score')
            # print(f"sentence_starts: {sentence_starts}")
            left_part = response_text.find('>', sentence_starts)
            # print(f"left_part: {left_part}")
            righ_part = response_text.find('<', left_part)
            # print(f"righ_part: {righ_part}")
            score = response_text[left_part + 1:righ_part]
            # print(f"score_str: {score}")
            score = float(score)
            print(f"score_float: {score}")
        except Exception as e:
            print(f"error in convert response text: {e}")
            score = 0
    except Exception as e:
        print(f"error in request: {e}")
        score = 0
    return score


def get_sp500():
    score = 0
    print("***** Start s&p500 getting process")
    try:
        url = "https://www.tipranks.com/index/spx"
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }
        r = requests.get(url, headers=headers)
        print(f"r.ok: {r.ok}")
        if not r.ok:
            score = 0
        try:
            response_text = r.text
            # print(f"response_text: {response_text}")
            sentence_starts = response_text.find('quote-market-notice')
            # print(f"sentence_starts: {sentence_starts}")
            left_part = response_text[:sentence_starts]
            # print(f"left_part: {left_part}")
            righ_part = response_text.find(')', left_part)
            # print(f"righ_part: {righ_part}")
            score = response_text[left_part + 1:righ_part]
            # print(f"score_str: {score}")
            score = float(score)
            print(f"score_float: {score}")
        except Exception as e:
            print(f"error in convert response text: {e}")
            score = 0
    except Exception as e:
        print(f"error in request: {e}")
        score = 0
    return score


if __name__ == '__main__':
    # s = get_stock_invest_rank_for_ticker('bkh')
    a = get_sp500()
# get_stock_invest_rank_for_ticker('bkh')
