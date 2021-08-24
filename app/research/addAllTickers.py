import json
import ssl
import urllib
from urllib.request import urlopen

server_url = "https://www.algotrader.company/"
apikey = 'f6003a61d13c32709e458a1e6c7df0b0'
url = ("https://financialmodelingprep.com/api/v3/stock/list?apikey=" + apikey)
context = ssl._create_unverified_context()
response = urlopen(url, context=context)
data = response.read().decode("utf-8")
parsed = json.loads(data)
needed = []
print("finished download")
i = 1
for s in parsed:
    i = i + 1
    print('Adding' + s['symbol'] + str(i) + 'from ' + str(len(parsed)))
    ticker = s['symbol']
    data = urllib.parse.urlencode({"ticker_to_add": ticker,
                                   })
    data = data.encode('ascii')

    url = server_url + "candidates/add_by_spider"
    response = urllib.request.urlopen(url, data)
    print(s['symbol'] + 'Added')

print('finished adding')
