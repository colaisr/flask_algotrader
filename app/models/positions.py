from datetime import datetime

from . import TickerData
import app.models.fgi_score
from .. import db
from sqlalchemy import text


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
    exec_id_buy = db.Column('exec_id_buy', db.String)
    exec_id_sld = db.Column('exec_id_sld', db.String)
    buying_algotrader_rank = db.Column('buying_algotrader_rank', db.Float)
    emotion_on_buy = db.Column('emotion_on_buy', db.Integer)

    def update_position(self):
        updating_result = "Nothing"
        if self.last_exec_side == 'BOT':
            # p = Position.query.filter(Position.email == self.email, Position.ticker == self.ticker) \
            #     .filter(or_(Position.last_exec_side == 'BOT',
            #                 Position.last_exec_side == 'SLD' and Position.opened.date() == datetime.now().date())) \
            #     .first()
            query_text = f"SELECT * FROM Positions WHERE Positions.`email` = '{self.email}' AND Positions.`ticker` = '{self.ticker}' AND (Positions.`last_exec_side` = 'BOT' OR (Positions.`last_exec_side` = 'SLD' AND DATE(Positions.`opened`) = DATE(NOW())))"
            p = db.session.query(Position).from_statement(text(query_text)).first()
            if p is None:
                # adding market data
                m_data = TickerData.query.filter_by(ticker=self.ticker).order_by(
                    TickerData.updated_server_time.desc()).first()
                app.models.fgi_score.Fgi_score
                fgi = app.models.fgi_score.Fgi_score.query.order_by(app.models.fgi_score.Fgi_score.score_time.desc()).first()
                self.buying_tiprank = m_data.tipranks
                self.buying_yahoo_rank = m_data.yahoo_rank
                self.buying_underprice = m_data.under_priced_pnt
                self.buying_twelve_month_momentum = m_data.twelve_month_momentum
                self.buying_average_drop = m_data.yahoo_avdropP
                self.buying_average_spread = m_data.yahoo_avspreadP
                self.buying_fmp_rating = m_data.fmp_rating
                self.buying_fmp_score = m_data.fmp_score
                self.buying_algotrader_rank = m_data.algotrader_rank
                self.emotion_on_buy = fgi.fgi_value

                db.session.add(self)
                updating_result = "new_buy"
                p = Position.query.filter_by(email=self.email, ticker=self.ticker, last_exec_side='BOT').first()
            else:
                pass
        else:
            p = Position.query.filter_by(email=self.email, ticker=self.ticker, last_exec_side='BOT').first()
            if p is not None:
                p.exec_id_sld = self.exec_id_sld
                p.close_price = self.close_price
                p.closed = self.closed
                p.last_exec_side = self.last_exec_side
                p.profit = p.close_price * p.stocks - p.open_price * p.stocks
                updating_result = "new_sell"
        db.session.commit()
        return updating_result, p

    def toDictionary(self):
        d = self.__dict__
        d.pop('_sa_instance_state', None)
        d.__setitem__('opened', datetime.isoformat(self.opened))
        if self.closed is not None:
            d.__setitem__('closed', datetime.isoformat(self.closed))
        else:
            d.__setitem__('closed', '')
        return d
