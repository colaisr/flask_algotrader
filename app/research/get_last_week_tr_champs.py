import json
import ssl
import urllib
from urllib.request import urlopen

server_url = "https://www.algotrader.company/"

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

for c in champs_list:
    data = urllib.parse.urlencode({"ticker_to_add": c['ticker'], })
    data = data.encode('ascii')

    url = server_url + "candidates/add_by_spider"
    response = urllib.request.urlopen(url, data)
