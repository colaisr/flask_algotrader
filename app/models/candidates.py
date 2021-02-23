from .. import db

class Candidate(db.Model):
    __tablename__ = 'Candidates'
    __bind_key__ = 'db_clients'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)
    ticker = db.Column('ticker', db.String)
    description = db.Column('description', db.String)

    def update_position(self):
        candidate = Candidate.query.filter((Candidate.email==self.email) & (Candidate.ticker==self.ticker)).first()

        if candidate is None:
            db.session.add(self)
        db.session.commit()