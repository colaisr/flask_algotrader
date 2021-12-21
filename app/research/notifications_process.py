import sys
import urllib
import ssl
import json
import time
from urllib.request import urlopen
from datetime import datetime

#***************************************
#***************************************
# RUN IN UTC FORMAT
#***************************************
#***************************************

# server_url = 'http://127.0.0.1:5000/'
server_url = 'https://www.stockscore.company/'


def update_process_status(percent, status):
    #status: 0 - started, 1 - run, 2 - ended
    data = urllib.parse.urlencode({
        "status": status,
        "percent": percent
    })
    data = data.encode('ascii')
    url = server_url + "research/update_process_status"
    try:
        response = urllib.request.urlopen(url, data)
    except Exception as e:
        print("update process status failed. ", e)


def get_all_users():
    _url = (f"{server_url}research/all_users_for_notifications")
    _context = ssl._create_unverified_context()
    _response = urlopen(_url, context=_context)
    _data = _response.read().decode("utf-8")
    _parsed = json.loads(_data)
    return _parsed


def notifications_process():
    start_time = datetime.now()
    print("****Starting notifications process  " + start_time.strftime("%d/%m/%Y %H:%M:%S") + "****")

    try:
        users = get_all_users()
        update_process_status(0, 0)

        error_status = 0

        p = 100 / len(users)
        min_step = 2

        update_times = []
        counter = 1
        percent = 2

        for u in users:
            try:
                start_update_time = time.time()
                print(f'Notifications for : {u} stamp: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
                _data = urllib.parse.urlencode({"user": u})
                _data = _data.encode('ascii')
                _url = server_url + "connections/tickers_notifications"
                _response = urllib.request.urlopen(_url, _data)
                end_update_time = time.time()
                print(f"Updated stamp: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
                _responseJSON = json.loads(_response.read())

                if _responseJSON["status"] == 0:
                    delta = end_update_time - start_update_time
                    update_times.append(delta)
                else:
                    counter -= 1

                if counter * p >= percent:
                    update_process_status(percent, 1)
                    percent += min_step
            except Exception as e:
                print(f"Error in for cycle: {e}")
                error_status = 1
                counter -= 1
            counter += 1

        update_process_status(percent, 2)

        avg = sum(update_times) / len(update_times) if len(update_times) != 0 else 0
        end_time = datetime.now()
        print(f"***All notifications sended {end_time.strftime('%d/%m/%Y %H:%M:%S')}")
        print("***Save last time update***")

        data = urllib.parse.urlencode({
            "error_status": error_status,
            "start_time": start_time,
            "end_time": end_time,
            "num_of_users": len(users),
            "num_users_received": len(update_times),
            "avg_update_times": avg
        })
        data = data.encode('ascii')
        url = server_url + "research/save_process_data"
        try:
            response = urllib.request.urlopen(url, data)
            print("***Date updated***")
        except Exception as e:
            print("Saving time update data failed. ", e)
        print("*************************************************")
    except:
        print("Notifications process error. ", sys.exc_info()[0])

    print("****Notifications process finished " + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + "****")

#*****************************************************************
#*****************************************************************
#*****************************************************************

notifications_process()
