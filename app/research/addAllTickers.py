import json
import ssl
import urllib
from urllib.request import urlopen
server_url="http://colak.eu.pythonanywhere.com/"
apikey='f6003a61d13c32709e458a1e6c7df0b0'
url = ("https://financialmodelingprep.com/api/v3/stock/list?apikey=" + apikey)
context = ssl._create_unverified_context()
response = urlopen(url, context=context)
data = response.read().decode("utf-8")
parsed = json.loads(data)
needed=[]
for s in parsed:
    ticker=s['symbol']
    data = urllib.parse.urlencode({"ticker_to_add": ticker,
                                   })
    data = data.encode('ascii')

    url =server_url+"candidates/add_by_spider"
    response = urllib.request.urlopen(url, data)
    i = 2


url = ("https://www.tipranks.com/api/Screener/GetStocks/?break=1111111111111&country=US&page=1&scoreChangeDate=2&sortBy=1&sortDir=2&tipranksScore=5")
context = ssl._create_unverified_context()
response = urlopen(url, context=context)
data = response.read().decode("utf-8")
parsed = json.loads(data)
pages=(parsed['count']/20)
champs_list=[]
for p in range(int(pages)):
    url = (
        "https://www.tipranks.com/api/Screener/GetStocks/?break=1111111111111&country=US&page="+str(p+1)+"&scoreChangeDate=2&sortBy=1&sortDir=2&tipranksScore=5")
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    parsed = json.loads(data)
    for c in parsed['data']:
        ticker=c['ticker']
        champs_list.append(c)

for c in champs_list:
    data = urllib.parse.urlencode({"ticker_to_add": c['ticker'],
                                   })
    data = data.encode('ascii')

    url =server_url+"candidates/add_by_spider"
    response = urllib.request.urlopen(url, data)








import json
import ssl
from urllib.request import urlopen




if __name__ == '__main__':
    url = ("https://financialmodelingprep.com/api/v3/stock/list?apikey="+apikey)
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    parsed=json.loads(data)
    i=2


def get_fmp_pe_for_ticker(s):
    url = ("https://financialmodelingprep.com/api/v3/ratios-ttm/"+s+"?apikey="+apikey)
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    parsed=json.loads(data)
    pe=parsed[0]['peRatioTTM']
    return pe

def get_fmp_ratings_score_for_ticker(s):
    try:
        url = ("https://financialmodelingprep.com/api/v3/rating/"+s+"?apikey="+apikey)
        context = ssl._create_unverified_context()
        response = urlopen(url, context=context)
        data = response.read().decode("utf-8")
        parsed=json.loads(data)
        if len(parsed)>0:
            rating=parsed[0]['rating']
            score = parsed[0]['ratingScore']
            return rating,score
        else:
            return 'N',1
    except:
        return 'NE',0