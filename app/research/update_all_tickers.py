import json
import ssl
import urllib
from urllib.request import urlopen
server_url="http://colak.eu.pythonanywhere.com/"

def get_all_tickers():
    url = (server_url+"/research/alltickers")
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    parsed=json.loads(data)

    return parsed

tickers=get_all_tickers()
for t in tickers:
    data = urllib.parse.urlencode({"ticker_to_update": t})
    data = data.encode('ascii')

    url =server_url+"/research/updatemarketdataforcandidate"
    response = urllib.request.urlopen(url, data)
    u=3
done=2
