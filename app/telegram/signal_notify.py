import os
import ssl
import urllib
from urllib.request import urlopen
import telebot

def send_telegram_signal_message_OLD(param):
    param=param.replace(" ","%20")
    tk="1956877943:AAHdOybFQOLBwAX85xZOgLYgW2NI-3k3_jc"
    url = "https://api.telegram.org/bot"+tk+"/sendMessage?chat_id=@algotrader_signals&text="+param
    context = ssl._create_unverified_context()
    response = urlopen(url, context=context)
    r=3

def send_telegram_signal_message(param):
    tk=os.environ.get('TELEGRAM_KEY')
    bot = telebot.TeleBot(tk)
    chat_id=os.environ.get('TELEGRAM_CHANEL')
    bot.send_message(chat_id, param)
    r=3


if __name__ == '__main__':
    send_telegram_signal_message("hello all")