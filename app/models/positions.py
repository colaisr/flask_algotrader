

from .. import db
class Position(db.Model):
    __tablename__ = 'Positions'
    __bind_key__ = 'db_clients'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)
    ticker = db.Column('ticker', db.String)
    opened = db.Column('opened', db.DateTime)
    closed = db.Column('closed', db.DateTime)
    open_price = db.Column('open_price', db.Float)
    close_price = db.Column('close_price', db.Float)
    stocks = db.Column('stocks', db.Integer)
    last_exec_side = db.Column('last_exec_side', db.String)
    profit = db.Column('profit', db.Float)

    def update_position(self):
        if self.last_exec_side=='BOT':
            db.session.add(self)
        else:
            p = Position.query.filter_by(email=self.email,ticker=self.ticker).order_by(Position.id.desc()).first()
            if p is not None:
                p.close_price=self.close_price
                p.closed = self.closed
                p.last_exec_side=self.last_exec_side
                p.profit = self.close_price*self.stocks-p.open_price*p.stocks
        db.session.commit()




