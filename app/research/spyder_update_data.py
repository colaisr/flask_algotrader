import json
import ssl
import urllib
from urllib.request import urlopen
from datetime import datetime
import time

#***************************************
#***************************************
# RUN IN UTC FORMAT
#***************************************
#***************************************

# server_url = "http://127.0.0.1:5000/"
server_url = "https://www.algotrader.company/"


def get_all_tickers():
    print("Getting all necessary tickers from Algotrader server")
    _url = (f"{server_url}research/alltickers")
    _context = ssl._create_unverified_context()
    _response = urlopen(_url, context=_context)
    _data = _response.read().decode("utf-8")
    _parsed = json.loads(_data)
    print(f"Got all {str(len(_parsed))} tickers from server- starting to update...")
    return _parsed


def update_market_data(_tickers, _update_times, _research_error_tickers, _error_tickers):
    # test_tickers = _tickers[:5]
    _already_updated_tickers = 0
    _error_status = 0
    for t in _tickers:
        try:
            start_update_time = time.time()
            print(f'Updating data for : {t} stamp: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
            _data = urllib.parse.urlencode({"ticker_to_update": t})
            _data = _data.encode('ascii')
            _url = server_url + "research/updatemarketdataforcandidatespider"
            _response = urllib.request.urlopen(_url, _data)
            end_update_time = time.time()
            print(f"Updated stamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
            _responseJSON = json.loads(_response.read())

            if _responseJSON["status"] == 0:
                delta = end_update_time - start_update_time
                _update_times.append(delta)
            elif _responseJSON["status"] == 1:
                _already_updated_tickers += 1
                _research_error_tickers.append({t: _responseJSON["sections"]})
            else:
                _research_error_tickers.append({t: [_responseJSON["error"]]})
        except Exception as e:
            # print(f"Error in for cycle: {e}")
            _error_status = 1
            _error_tickers.append(t)
    return _already_updated_tickers, _error_status


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
# already_updated_tickers = 0
error_tickers = []
research_error_tickers = []
update_times = []

already_updated_tickers, error_status = update_market_data(tickers, update_times, research_error_tickers, error_tickers)

num_of_tickers = len(tickers)

if len(error_tickers) > 0 or len(research_error_tickers) > 0:
    tickers = []
    tickers = error_tickers
    error_tickers = []
    if len(research_error_tickers) > 0:
        for item in research_error_tickers:
            for k, v in item.items():
                tickers.append(k)
        research_error_tickers = []
    already_updated_tickers, error_status = update_market_data(tickers, update_times, research_error_tickers, error_tickers)

if error_status == 1:
    print(f"Update MarketData error. Tickers: {json.dumps(error_tickers)}")

avg = sum(update_times)/len(update_times) if len(update_times) != 0 else 0
end_time = datetime.now()
print(f"***All tickers successfully updated {end_time.strftime('%d/%m/%Y %H:%M:%S')}")
print("***Save last time update***")

data = urllib.parse.urlencode({
                                "error_status": error_status,
                                "start_time": start_time,
                                "end_time": end_time,
                                "num_of_positions": num_of_tickers,
                                "error_tickers": json.dumps(error_tickers),
                                "research_error_tickers": json.dumps(research_error_tickers),
                                "updated_tickers": len(update_times),
                                "already_updated_tickers": already_updated_tickers,
                                "avg_update_times": avg,
                                "error_tickers_num": len(research_error_tickers) + len(error_tickers)
                              })
data = data.encode('ascii')
url = server_url + "research/savelasttimeforupdatedata"
try:
    response = urllib.request.urlopen(url, data)
    print("***Date updated***")
except Exception as e:
    print("Saving time update data failed. ", e)
print("*************************************************")
