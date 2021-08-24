import json
import ssl
import urllib
from urllib.request import urlopen
from datetime import datetime

server_url = "https://www.algotrader.company/"
result = " Updater spider failed a work successfully"


def get_all_tickers():
    print("Getting all necessary tickets from Algotrader server")
    url = (server_url + "/research/alltickers")
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    parsed = json.loads(data)
    print("Got all " + str(len(parsed)) + " tickers from server- starting to update...")
    return parsed


now = datetime.now()
print("****Starting Updater spider for all existing Candidates" + now.strftime("%d/%m/%Y %H:%M:%S"))
tickers = get_all_tickers()

for s in tickers:
    print('Adding' + s + 'from ' + str(len(tickers)))
    ticker = s
    data = urllib.parse.urlencode({"ticker_to_add": ticker,
                                   })
    data = data.encode('ascii')

    url = server_url + "candidates/add_by_spider"
    response = urllib.request.urlopen(url, data)
    print(s + 'Added')

print('finished alighning')
