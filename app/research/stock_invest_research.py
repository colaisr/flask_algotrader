import requests


def get_stock_invest_rank_for_ticker(ticker):
    score = 0
    log = "***** Start stockinvest getting process"
    print("***** Start stockinvest getting process")
    try:
        url = "https://stockinvest.us/stock/" + ticker
        headers = {
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36"
        }
        r = requests.get(url, headers=headers)
        log += f"/n******* r.ok: {r.ok} *******"
        print(f"r.ok: {r.ok}")
        if not r.ok:
            score = 0
        try:
            response_text = r.text
            sentence_starts = response_text.find('Current score')
            left_part = response_text.find('>', sentence_starts)
            righ_part = response_text.find('<', left_part)
            score = response_text[left_part + 1:righ_part]
            score = float(score)
            log += f"/n***** score: {score} *****"
            print(f"score: {score}")
        except Exception as e:
            log += f"/n***** error in convert response text: {e} *****"
            print(f"error in convert response text: {e}")
            score = 0
    except Exception as e:
        log += f"/n***** error in request: {e} *****"
        print(f"error in request: {e}")
        score = 0
    return score


if __name__ == '__main__':
    s = get_stock_invest_rank_for_ticker('bkh')

get_stock_invest_rank_for_ticker('bkh')
