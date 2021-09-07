import json
import ssl
import urllib
from urllib.request import urlopen
from datetime import datetime

# server_url = "http://127.0.0.1:5000/"
server_url = "https://www.algotrader.company/"
error_message = ""
error_status = 0


def get_all_tickers():
    print("Getting all necessary tickets from Algotrader server")
    _url = (f"{server_url} research/alltickers")
    _context = ssl._create_unverified_context()
    _response = urlopen(_url, context=_context)
    _data = _response.read().decode("utf-8")
    _parsed = json.loads(_data)
    print(f"Got all {str(len(_parsed))} tickers from server- starting to update...")
    return _parsed


now = datetime.now()
print("*************************************************")
print(f"****Starting spider for last week champs {now.strftime('%d/%m/%Y %H:%M:%S')} ****")
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
            print(f"Sending {c['ticker']} {now.strftime('%d/%m/%Y %H:%M:%S')}")
            data = urllib.parse.urlencode({"ticker_to_add": c['ticker'], })
            data = data.encode('ascii')

            url = server_url + "candidates/add_by_spider"
            response = urllib.request.urlopen(url, data)
            now = datetime.now()
            print(f"Sent stamp {now.strftime('%d/%m/%Y %H:%M:%S')}")
    except Exception as e:
        print(f"GetLastWeekChamp error. {e}")
    now = datetime.now()
    print(f"****End spider for last week champs {now.strftime('%d/%m/%Y %H:%M:%S')} ****")
except Exception as e:
    print("GetLastWeekChamp error. ", str(e))

start_time = datetime.now()
print(f'****Starting Updater spider for all existing Candidates {start_time.strftime("%d/%m/%Y %H:%M:%S")}')
tickers = get_all_tickers()
num_of_positions = 0
error_tickets = []
for t in tickers:
    try:
        start_update_time = datetime.now()
        print(f'Updating data for : {t} stamp: {start_update_time.strftime("%d/%m/%Y %H:%M:%S")}')
        data = urllib.parse.urlencode({"ticker_to_update": t})
        data = data.encode('ascii')
        url = server_url + "research/updatemarketdataforcandidate"
        response = urllib.request.urlopen(url, data)
        end_update_time = datetime.now()
        print(f"Updated stamp: {end_update_time.strftime('%d/%m/%Y %H:%M:%S')}")
        num_of_positions += 1
    except Exception as e:
        error_status = 1
        error_tickets.append(t)

if error_status == 1:
    print(f"Update MarketData error. Tickets: {json.dumps(error_tickets)}")

end_time = datetime.now()
print(f"***All tickers successfully updated {end_time.strftime('%d/%m/%Y %H:%M:%S')}")
print("***Save last time update***")

data = urllib.parse.urlencode({
                                "error_status": error_status,
                                "error_message": error_message,
                                "start_time": start_time,
                                "end_time": end_time,
                                "num_of_positions": num_of_positions,
                                "error_tickets": json.dumps(error_tickets)
                              })
data = data.encode('ascii')
url = server_url + "research/savelasttimeforupdatedata"
try:
    response = urllib.request.urlopen(url, data)
    print("***Date updated***")
except Exception as e:
    print("Saving time update data failed. ", e)
print("*************************************************")
