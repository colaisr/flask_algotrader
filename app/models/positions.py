

from .. import db
class Position(db.Model):
    __tablename__ = 'Positions'
    __bind_key__ = 'db_clients'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)
    updated = db.Column('updated', db.DateTime)
    opened = db.Column('opened', db.DateTime)
    closed = db.Column('closed', db.DateTime)
    open_price = db.Column('open_price', db.Float)
    close_price = db.Column('close_price', db.Float)
    candidate_state_on_open = db.relationship("CandidateState", uselist=False, back_populates="position")


class CandidateState(db.Model):
    __tablename__ = 'CandidateStates'
    __bind_key__ = 'db_clients'
    id = db.Column('id', db.Integer, primary_key=True)
    position_id = db.Column(db.Integer, db.ForeignKey('Positions.id'))
    position = db.relationship("Position", back_populates="candidate_state_on_open")
    ticker = db.Column('ticker', db.String)
    ask_price = db.Column('ask_price', db.Float)
    bid_price = db.Column('bid_price', db.Float)
    yahoo_rating = db.Column('yahoo_rating', db.Integer)
    tipranks_rating = db.Column('tipranks_rating', db.Integer)
    snapshoted_at = db.Column('snapshoted_at', db.DateTime)