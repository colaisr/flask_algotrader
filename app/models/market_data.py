from datetime import datetime, date
import json

from .. import db


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


class TickerData(db.Model):
    __tablename__ = 'Tickersdata'
    # __bind_key__ = 'db_market_data'
    id = db.Column('id', db.Integer, primary_key=True)
    ticker = db.Column('ticker', db.String)
    yahoo_avdropP = db.Column('yahoo_avdropP', db.Float)
    yahoo_avspreadP = db.Column('yahoo_avspreadP', db.Float)
    tipranks = db.Column('tipranks', db.Integer)
    yahoo_rank = db.Column('yahoo_rank', db.Float)
    stock_invest_rank = db.Column('stock_invest_rank', db.Float)
    under_priced_pnt = db.Column('under_priced_pnt', db.Float)
    twelve_month_momentum = db.Column('twelve_month_momentum', db.Float)
    target_mean_price = db.Column('target_mean_price', db.Float)
    max_intraday_drop_percent = db.Column('max_intraday_drop_percent', db.Float)
    beta = db.Column('beta', db.Float)
    fmp_rating = db.Column('fmp_rating', db.String)
    fmp_score = db.Column('fmp_score', db.Integer)
    updated_server_time = db.Column('updated_server_time', db.DateTime)
    algotrader_rank = db.Column('algotrader_rank', db.Float)

    def add_ticker_data(self):
        db.session.add(self)
        db.session.commit()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def toDictionary(self):
        d = {}
        d['ticker'] = self.ticker
        d['yahoo_avdropP'] = self.yahoo_avdropP
        d['yahoo_avspreadP'] = self.yahoo_avspreadP
        d['tipranks'] = self.tipranks
        d['yahoo_rank'] = self.yahoo_rank
        d['algotrader_rank'] = self.algotrader_rank
        d['under_priced_pnt'] = self.under_priced_pnt
        d['twelve_month_momentum'] = self.twelve_month_momentum
        d['target_mean_price'] = self.target_mean_price
        d['max_intraday_drop_percent'] = self.max_intraday_drop_percent
        d['beta'] = self.beta
        d['fmp_rating'] = self.fmp_rating
        d['fmp_score'] = self.fmp_score
        d['stock_invest_rank'] = self.stock_invest_rank
        d['updated_server_time'] = datetime.isoformat(self.updated_server_time)
        return d


class LastUpdateSpyderData(db.Model):
    __tablename__ = 'LastUpdateSpyderData'
    id = db.Column('id', db.Integer, primary_key=True)
    start_process_time = db.Column('start_process_time', db.DateTime)
    end_process_time = db.Column('end_process_time', db.DateTime)
    last_update_date = db.Column('last_update_date', db.DateTime)
    avg_time_by_position = db.Column('avg_time_by_position', db.Float)
    num_of_positions = db.Column('num_of_positions', db.BigInteger)
    error_status = db.Column('error_status', db.Boolean)
    error_tickers = db.Column('error_tickers', db.String)
    research_error_tickers = db.Column('research_error_tickers', db.String)
    already_updated_tickers = db.Column('already_updated_tickers', db.BigInteger)
    updated_tickers = db.Column('updated_tickers', db.BigInteger)
    error_tickers_num = db.Column('error_tickers_num', db.BigInteger)

    def update_data(self):
        data = LastUpdateSpyderData.query.filter(LastUpdateSpyderData.start_process_time == self.start_process_time,
                                                 LastUpdateSpyderData.end_process_time == self.end_process_time).first()
        if data is None:
            db.session.add(self)
        db.session.commit()
