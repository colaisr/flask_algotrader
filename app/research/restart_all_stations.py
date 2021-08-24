import urllib
from urllib.request import urlopen

server_url = "https://www.algotrader.company/"

url = server_url + "/connections/restart_all_stations"

data = urllib.parse.urlencode({"requester": 'admin spider'})
data = data.encode('ascii')
response = urllib.request.urlopen(url, data)
