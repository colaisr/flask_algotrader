from .. import db


class TelegramSignal(db.Model):
    __tablename__ = 'TelegramSignals'
    id = db.Column('id', db.Integer, primary_key=True)
    ticker = db.Column('ticker', db.String)
    transmitted = db.Column('transmitted', db.Boolean)
    received = db.Column('received', db.DateTime)

    def add_signal(self):
        signal = TelegramSignal.query.filter((TelegramSignal.ticker == self.ticker) & (TelegramSignal.received == self.received)).first()
        # signal = TelegramSignal.query.filter((TelegramSignal.ticker == self.ticker)).first()

        if signal is None:
            db.session.add(self)
            db.session.commit()
            return True
        else:
            return False