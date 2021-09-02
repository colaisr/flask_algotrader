from datetime import datetime

from . import TickerData
from .. import db
from sqlalchemy import or_


class Position(db.Model):
    __tablename__ = 'Positions'
    # __bind_key__ = 'db_clients'
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
    buying_tiprank = db.Column('buying_tiprank', db.Integer)
    buying_yahoo_rank = db.Column('buying_yahoo_rank', db.Float)
    buying_underprice = db.Column('buying_underprice', db.Float)
    buying_twelve_month_momentum = db.Column('buying_twelve_month_momentum', db.Float)
    buying_average_drop = db.Column('buying_average_drop', db.Float)
    buying_average_spread = db.Column('buying_average_spread', db.Float)
    buying_fmp_rating = db.Column('buying_fmp_rating', db.String)
    buying_fmp_score = db.Column('buying_fmp_score', db.Integer)

    def update_position(self):
        updating_result = "Nothing"
        if self.last_exec_side == 'BOT':
            p = Position.query.filter(Position.email == self.email, Position.ticker == self.ticker) \
                .filter(or_(Position.last_exec_side == 'BOT',
                            Position.last_exec_side == 'SLD' and Position.opened.date() == datetime.now().date())) \
                .first()
            if p is None:
                # adding market data
                m_data = TickerData.query.filter_by(ticker=self.ticker).order_by(
                    TickerData.updated_server_time.desc()).first()
                self.buying_tiprank = m_data.tipranks
                self.buying_yahoo_rank = m_data.yahoo_rank
                self.buying_underprice = m_data.under_priced_pnt
                self.buying_twelve_month_momentum = m_data.twelve_month_momentum
                self.buying_average_drop = m_data.yahoo_avdropP
                self.buying_average_spread = m_data.yahoo_avspreadP
                self.buying_fmp_rating = m_data.fmp_rating
                self.buying_fmp_score = m_data.fmp_score

                db.session.add(self)
                updating_result = "new_buy"
                p = Position.query.filter_by(email=self.email, ticker=self.ticker, last_exec_side='BOT').first()
            else:
                pass
        else:
            p = Position.query.filter_by(email=self.email, ticker=self.ticker, last_exec_side='BOT').first()
            if p is not None:
                p.close_price = self.close_price
                p.closed = self.closed
                p.last_exec_side = self.last_exec_side
                p.profit = p.close_price * p.stocks - p.open_price * p.stocks
                updating_result = "new_sell"
        db.session.commit()
        return updating_result, p

    def toDictionary(self):
        d = {}
        d['ticker'] = self.ticker
        d['opened'] = datetime.isoformat(self.opened)
        return d
