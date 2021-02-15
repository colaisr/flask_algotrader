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
    __bind_key__ = 'db_market_data'
    id = db.Column('id', db.Integer, primary_key=True)
    ticker = db.Column('ticker', db.String)
    yahoo_avdropP = db.Column('yahoo_avdropP', db.Float)
    yahoo_avspreadP = db.Column('yahoo_avspreadP', db.Float)
    tipranks = db.Column('tipranks', db.Integer)
    updated = db.Column('updated', db.DateTime)
    updated_by_user = db.Column('updated_by_user', db.String)

    def update_ticker_data(self):
        td = TickerData.query.filter_by(ticker=self.ticker).first()
        if td is None:
            db.session.add(self)
        else:
            td.yahoo_avdropP=self.yahoo_avdropP
            td.yahoo_avspreadP = self.yahoo_avspreadP
            td.tipranks=self.tipranks
            td.updated = self.updated
        db.session.commit()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def toDictionary(self):
        d={}
        d['ticker']=self.ticker
        d['yahoo_avdropP'] = self.yahoo_avdropP
        d['yahoo_avspreadP'] = self.yahoo_avspreadP
        d['tipranks'] = self.tipranks
        # d['updated'] = json.dumps(self.updated, default=json_serial)
        d['updated'] = datetime.isoformat(self.updated)

        return d