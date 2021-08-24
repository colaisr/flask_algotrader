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
for t in tickers:
    print("Updating data for : " + t)
    data = urllib.parse.urlencode({"ticker_to_update": t})
    data = data.encode('ascii')

    url = server_url + "/research/updatemarketdataforcandidate"
    response = urllib.request.urlopen(url, data)
    print("Updated")
now = datetime.now()
print("***All tickers successfully updated" + now.strftime("%d/%m/%Y %H:%M:%S"))
