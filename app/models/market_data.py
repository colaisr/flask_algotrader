from datetime import datetime,date
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
    yahoo_rank=db.Column('yahoo_rank', db.Float)
    under_priced_pnt = db.Column('under_priced_pnt', db.Float)
    fmp_rating = db.Column('fmp_rating', db.String)
    fmp_score = db.Column('fmp_score', db.Integer)
    updated_server_time=db.Column('updated_server_time', db.DateTime)


    def add_ticker_data(self):

        db.session.add(self)
        db.session.commit()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def toDictionary(self):
        d={}
        d['ticker']=self.ticker
        d['yahoo_avdropP'] = self.yahoo_avdropP
        d['yahoo_avspreadP'] = self.yahoo_avspreadP
        d['tipranks'] = self.tipranks
        d['yahoo_rank']=self.yahoo_rank
        d['under_priced_pnt'] = self.under_priced_pnt
        d['fmp_rating'] = self.fmp_rating
        d['fmp_score'] = self.fmp_score
        d['updated_server_time'] = datetime.isoformat(self.updated_server_time)
        return d