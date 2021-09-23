import datetime

import yfinance as yf


def get_yahoo_stats_for_ticker(s):

    df = yf.download(s, period="1y")
    df['drop'] = df['Open'] - df['Low']
    df['dropP'] = df['drop'] / df['Open'] * 100
    df['diffD'] = df['Low'] - df['High']
    df['diffD'] = df['diffD'].abs()
    df['diffP'] = df['diffD'] / df['Open'] * 100

    max_intraday_drop_percent=df['dropP'].max()
    avdropP = df["dropP"].mean()
    avChange = df["diffP"].mean()

    return avdropP, avChange,max_intraday_drop_percent


def get_info_for_ticker(s):
    # t=yf.Ticker(s)
    inf = yf.Ticker(s).info

    return inf


def get_current_snp_change_percents():
    s='^spx'
    inf=yf.Ticker(s).info
    current_price=inf['regularMarketPrice']
    prev_close=inf['previousClose']
    difference=current_price-prev_close
    difference_percents=100*difference/prev_close
    return difference_percents

if __name__ == '__main__':
    # get_yahoo_stats_for_ticker('abcl')
    # get_info_for_ticker('es=f')
    r=3

