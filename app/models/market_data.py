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
    fmp_pe = db.Column('fmp_pe', db.Float)
    fmp_rating = db.Column('fmp_rating', db.String)
    fmp_score = db.Column('fmp_score', db.Integer)
    updated_server_time=db.Column('updated_server_time', db.DateTime)


    def update_ticker_data(self):
        td = TickerData.query.filter_by(ticker=self.ticker).first()
        if td is None:
            db.session.add(self)
        else:
            td.yahoo_avdropP=self.yahoo_avdropP
            td.yahoo_avspreadP = self.yahoo_avspreadP
            td.tipranks=self.tipranks
            td.fmp_pe=self.fmp_pe
            td.fmp_rating=self.fmp_rating
            td.fmp_score=self.fmp_score
            td.updated_server_time = self.updated_server_time

        db.session.commit()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def toDictionary(self):
        d={}
        d['ticker']=self.ticker
        d['yahoo_avdropP'] = self.yahoo_avdropP
        d['yahoo_avspreadP'] = self.yahoo_avspreadP
        d['tipranks'] = self.tipranks
        d['fmp_pe'] = self.fmp_pe
        d['fmp_rating'] = self.fmp_rating
        d['fmp_score'] = self.fmp_score
        d['updated_server_time'] = datetime.isoformat(self.updated_server_time)
        return d