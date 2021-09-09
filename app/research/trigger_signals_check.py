import json
import ssl
import urllib
from urllib.request import urlopen
from datetime import datetime
import time

#server_url = "http://127.0.0.1:5000/"
server_url = "https://www.algotrader.company/"


url = server_url + "connections/signals_check"
context = ssl._create_unverified_context()
response = urllib.request.urlopen(url,context=context)
r=2

