import yfinance as yf


def get_yahoo_stats_for_ticker(s):
    df = yf.download(s, period="1y")
    df['drop'] = df['Open'] - df['Low']
    df['dropP'] = df['drop'] / df['Open'] * 100
    df['diffD'] = df['Low'] - df['High']
    df['diffD'] = df['diffD'].abs()
    df['diffP'] = df['diffD'] / df['Open'] * 100

    avdropP = df["dropP"].mean()
    avChange = df["diffP"].mean()
    beta = yf.Ticker(s).info['beta']
    if beta is None:
        beta=0

    return avdropP, avChange,beta


def get_beta_for_ticker(s):

    beta = yf.Ticker(s).info['beta']
    if beta is None:
        beta=0

    return beta

if __name__ == '__main__':
    msft = yf.Ticker("th").info['beta']
    s=3