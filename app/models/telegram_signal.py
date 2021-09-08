from .. import db


class TelegramSignal(db.Model):
    __tablename__ = 'TelegramSignals'
    id = db.Column('id', db.Integer, primary_key=True)
    ticker = db.Column('ticker', db.String)
    transmitted = db.Column('transmitted', db.Boolean)
    received = db.Column('received', db.DateTime)
    signal_price = db.Column('signal_price', db.Float)
    target_price = db.Column('target_price', db.Float)
    profit_percent = db.Column('profit_percent', db.Float)
    target_met = db.Column('target_met', db.DateTime)
    days_to_get = db.Column('days_to_get', db.Integer)

    def add_signal(self):
        signal = TelegramSignal.query.filter((TelegramSignal.ticker == self.ticker) & (TelegramSignal.received == self.received)).first()
        # signal = TelegramSignal.query.filter((TelegramSignal.ticker == self.ticker)).first()

        if signal is None:
            db.session.add(self)
            db.session.commit()
            return True
        else:
            return False

    def update_signal(self):
        db.session.commit()