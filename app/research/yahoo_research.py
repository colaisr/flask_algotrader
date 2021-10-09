import yfinance as yf


def get_current_snp_change_percents():
    s = '^spx'
    inf = yf.Ticker(s).info
    current_price = inf['regularMarketPrice']
    prev_close = inf['previousClose']
    difference = current_price - prev_close
    difference_percents = 100 * difference / prev_close
    return difference_percents


def get_snp500_fails_intraday_lower_than(min):
    s = '^GSPC'
    df = yf.download(s, period="5y")
    df['drop'] = df['Low'] - df['Open']
    df['dropP'] = df['drop'] / df['Open'] * 100
    df = df[df['dropP'] < min]
    return df


if __name__ == '__main__':
    get_snp500_fails_intraday_lower_than(-4)
    # get_info_for_ticker('vmd')
    r = 3
