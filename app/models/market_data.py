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
    yahoo_avdropP = db.Column('avdropP_fmp', db.Float)
    yahoo_avspreadP = db.Column('avspreadP_fmp', db.Float)
    buying_target_price_fmp=db.Column('buying_target_price_fmp', db.Float)
    tipranks = db.Column('rating_tr', db.Integer)
    yahoo_rank = db.Column('rating_yahoo', db.Float)
    stock_invest_rank = db.Column('rating_si', db.Float)
    under_priced_pnt = db.Column('under_priced_pnt_yahoo', db.Float)
    twelve_month_momentum = db.Column('twelve_month_momentum_tr', db.Float)
    target_mean_price = db.Column('target_mean_price_yahoo', db.Float)
    max_intraday_drop_percent = db.Column('max_intraday_drop_percent_fmp', db.Float)
    beta = db.Column('beta_yahoo', db.Float)
    fmp_rating = db.Column('rating_fmp', db.String)
    fmp_score = db.Column('score_fmp', db.Integer)
    updated_server_time = db.Column('updated_server_time', db.DateTime)
    algotrader_rank = db.Column('algotrader_rank', db.Float)

    tr_hedgeFundTrendValue = db.Column('hedgeFundTrendValue_tr', db.Float)
    tr_bloggerSectorAvg = db.Column('bloggerSectorAvg_tr', db.Float)
    tr_bloggerBullishSentiment = db.Column('bloggerBullishSentiment_tr', db.Float)
    tr_insidersLast3MonthsSum = db.Column('insidersLast3MonthsSum_tr', db.Float)
    tr_newsSentimentsBearishPercent = db.Column('newsSentimentsBearishPercent_tr', db.Float)
    tr_newsSentimentsBullishPercent = db.Column('newsSentimentsBullishPercent_tr', db.Float)
    tr_priceTarget = db.Column('priceTarget_tr', db.Float)
    tr_fundamentalsReturnOnEquity = db.Column('fundamentalsReturnOnEquity_tr', db.Float)
    tr_fundamentalsAssetGrowth = db.Column('fundamentalsAssetGrowth_tr', db.Float)
    tr_sma = db.Column('sma_tr', db.String)
    tr_analystConsensus = db.Column('analystConsensus_tr', db.String)
    tr_hedgeFundTrend = db.Column('hedgeFundTrend_tr', db.String)
    tr_insiderTrend = db.Column('insiderTrend_tr', db.String)
    tr_newsSentiment = db.Column('newsSentiment_tr', db.String)
    tr_bloggerConsensus = db.Column('bloggerConsensus_tr', db.String)

    def add_ticker_data(self):
        db.session.add(self)
        db.session.commit()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def toDictionary(self):
        d = self.__dict__
        d.pop('_sa_instance_state', None)
        d.__setitem__('updated_server_time', datetime.isoformat(self.updated_server_time))
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


class SpiderStatus(db.Model):
    __tablename__ = 'SpiderStatus'
    id = db.Column('id', db.Integer, primary_key=True)
    start_process_date = db.Column('start_process_date', db.DateTime)
    status = db.Column('status', db.String)
    percent = db.Column('percent', db.Float)

