from .. import db


class TickerData(db.Model):
    __tablename__ = 'Tickersdata'
    __bind_key__ = 'db_market_data'
    id = db.Column('id', db.Integer, primary_key=True)
    ticker = db.Column('ticker', db.String)
    yahoo_avdropP = db.Column('yahoo_avdropP', db.Float)
    yahoo_avspreadP = db.Column('yahoo_avspreadP', db.Float)
    tipranks = db.Column('tipranks', db.Integer)
    updated = db.Column('updated', db.DateTime)

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