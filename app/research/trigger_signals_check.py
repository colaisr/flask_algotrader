import ssl
import urllib
from urllib.request import urlopen

# server_url = "http://127.0.0.1:5000/"
server_url = "https://www.stockscore.company/"

url = server_url + "connections/market_fall_check"
context = ssl._create_unverified_context()
response = urllib.request.urlopen(url,context=context)
url = server_url + "connections/signals_check"
context = ssl._create_unverified_context()
response = urllib.request.urlopen(url,context=context)
url = server_url + "connections/signals_create"
context = ssl._create_unverified_context()
response = urllib.request.urlopen(url,context=context)

#notification process
url = server_url + "connections/notifications_process"
context = ssl._create_unverified_context()
response = urllib.request.urlopen(url, context=context)


