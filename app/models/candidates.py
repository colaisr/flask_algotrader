from .. import db

class Candidate(db.Model):
    __tablename__ = 'Candidates'
    # __bind_key__ = 'db_clients'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)
    ticker = db.Column('ticker', db.String)
    description = db.Column('description', db.String)
    enabled = db.Column('enabled', db.Boolean)

    def update_candidate(self):
        candidate = Candidate.query.filter((Candidate.email==self.email) & (Candidate.ticker==self.ticker)).first()

        if candidate is None:
            db.session.add(self)
        else:
            candidate.ticker=self.ticker
            candidate.description=self.description
            candidate.enabled=self.enabled
        db.session.commit()

    def delete_candidate(self):
        db.session.delete(self)
        db.session.commit()

    def change_enabled_state(self):
        if self.enabled:
            self.enabled=False
        else:
            self.enabled=True
        db.session.commit()

    def to_dictionary(self):
        d={}
        d['ticker']=self.ticker
        d['description'] = self.description
        return d