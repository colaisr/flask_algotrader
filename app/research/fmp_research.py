import json
import ssl
from urllib.request import urlopen

apikey = 'f6003a61d13c32709e458a1e6c7df0b0'


def get_fmp_pe_for_ticker(s):  # deprecated
    url = ("https://financialmodelingprep.com/api/v3/ratios-ttm/" + s + "?apikey=" + apikey)
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    parsed = json.loads(data)
    pe = parsed[0]['peRatioTTM']
    return pe


def get_fmp_ratings_score_for_ticker(s):
    try:
        url = ("https://financialmodelingprep.com/api/v3/rating/" + s + "?apikey=" + apikey)
        context = ssl._create_unverified_context()
        response = urlopen(url, context=context)
        data = response.read().decode("utf-8")
        parsed = json.loads(data)
        if len(parsed) > 0:
            rating = parsed[0]['rating']
            score = parsed[0]['ratingScore']
            return rating, score
        else:
            return 'N', 1
    except:
        return 'NE', 0


if __name__ == '__main__':
    r = get_fmp_ratings_score_for_ticker("csspf")
