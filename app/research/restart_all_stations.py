import urllib
from urllib.request import urlopen
server_url="http://colak.eu.pythonanywhere.com/"

url =server_url+"/connections/restart_all_stations"
response = urllib.request.urlopen(url)

