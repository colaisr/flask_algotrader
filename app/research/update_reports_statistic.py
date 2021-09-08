import sys
import urllib
from urllib.request import urlopen
from datetime import datetime

#***************************************
#***************************************
# RUN IN UTC FORMAT
#***************************************
#***************************************

# server_url = "http://127.0.0.1:5000/"
server_url = "https://www.algotrader.company/"

now = datetime.now()
print("****Starting update reports statistic process  " + now.strftime("%d/%m/%Y %H:%M:%S") + "****")

try:
    url = server_url + "research/update_reports_statistic"
    response = urllib.request.urlopen(url)
except:
    print("Update reports statistic process error. ", sys.exc_info()[0])

print("****Update reports statistic process finished " + now.strftime("%d/%m/%Y %H:%M:%S") + "****")