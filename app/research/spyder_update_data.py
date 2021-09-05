import json
import sys
import ssl
import urllib
from urllib.request import urlopen
from datetime import datetime

# server_url = "http://127.0.0.1:5000/"
server_url = "https://www.algotrader.company/"
error_message = "None"
error_status = 0


def get_all_tickers():
    print("Getting all necessary tickets from Algotrader server")
    _url = (server_url + "research/alltickers")
    _context = ssl._create_unverified_context()
    _response = urlopen(_url, context=_context)
    _data = _response.read().decode("utf-8")
    _parsed = json.loads(_data)
    print("Got all " + str(len(_parsed)) + " tickers from server- starting to update...")
    return _parsed


now = datetime.now()
print("*************************************************")
print("****Starting spider for last week champs  " + now.strftime("%d/%m/%Y %H:%M:%S") + "****")

try:
    url = (
        "https://www.tipranks.com/api/Screener/GetStocks/?break=1111111111111&country=US&page=1&scoreChangeDate=2&sortBy=1&sortDir=2&tipranksScore=5")
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    data = response.read().decode("utf-8")
    parsed = json.loads(data)
    pages = (parsed['count'] / 20)
    champs_list = []
    for p in range(int(pages)):
        url = ("https://www.tipranks.com/api/Screener/GetStocks/?break=1111111111111&country=US&page=" + \
               str(p + 1) + "&scoreChangeDate=2&sortBy=1&sortDir=2&tipranksScore=5")
        context = ssl._create_unverified_context()
        response = urlopen(url, context=context)
        data = response.read().decode("utf-8")
        parsed = json.loads(data)
        for c in parsed['data']:
            ticker = c['ticker']
            champs_list.append(c)
    try:
        for c in champs_list:
            now = datetime.now()
            print("Sending "+c['ticker'] + now.strftime("%d/%m/%Y %H:%M:%S"))
            data = urllib.parse.urlencode({"ticker_to_add": c['ticker'], })
            data = data.encode('ascii')

            url = server_url + "candidates/add_by_spider"
            response = urllib.request.urlopen(url, data)
            now = datetime.now()
            print("Sent stamp "+now.strftime("%d/%m/%Y %H:%M:%S"))
    except:
        print("GetLastWeekChamp error. ", sys.exc_info()[0])
    now = datetime.now()
    print("****End spider for last week champs  " + now.strftime("%d/%m/%Y %H:%M:%S") + "****")
except:
    print("GetLastWeekChamp error. ", sys.exc_info()[0])

now = datetime.now()
print("****Starting Updater spider for all existing Candidates" + now.strftime("%d/%m/%Y %H:%M:%S"))
tickers = get_all_tickers()
try:
    for t in tickers:
        now = datetime.now()
        print("Updating data for : " + t+ " stamp:"+now.strftime("%d/%m/%Y %H:%M:%S"))
        data = urllib.parse.urlencode({"ticker_to_update": t})
        data = data.encode('ascii')
        url = server_url + "research/updatemarketdataforcandidate"
        response = urllib.request.urlopen(url, data)
        now = datetime.now()
        print("Updated stamp:"+now.strftime("%d/%m/%Y %H:%M:%S"))
except:
    error_status = 1
    error_message = "Update MarketData error."
    print("Update MarketData for " + t + " error: ", sys.exc_info()[0])
now = datetime.now()
print("***All tickers successfully updated" + now.strftime("%d/%m/%Y %H:%M:%S"))
print("***Save last time update***")
data = urllib.parse.urlencode({"error_status": error_status, "error_message": error_message})
data = data.encode('ascii')
url = server_url + "research/savelasttimeforupdatedata"
try:
    response = urllib.request.urlopen(url, data)
    print("***Date updated***")
except:
    print("Saving time update data failed. ", sys.exc_info()[0])
print("*************************************************")
