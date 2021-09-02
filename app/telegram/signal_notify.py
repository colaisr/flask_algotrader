import ssl
import urllib
from urllib.request import urlopen

def send_telegram_signal_message(param):
    param=param.replace(" ","%20")
    tk="1956877943:AAHdOybFQOLBwAX85xZOgLYgW2NI-3k3_jc"
    url = "https://api.telegram.org/bot"+tk+"/sendMessage?chat_id=@algotrader_signals&text="+param
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    r=3


if __name__ == '__main__':
    send_telegram_signal_message("hello all")