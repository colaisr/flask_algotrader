from .. import db


class Candidate(db.Model):
    __tablename__ = 'Candidates'
    # __bind_key__ = 'db_clients'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)
    ticker = db.Column('ticker', db.String)
    reason = db.Column('reason', db.String)

    company_name = db.Column('company_name', db.String)
    exchange = db.Column('exchange', db.String)
    industry = db.Column('industry', db.String)
    sector = db.Column('sector', db.String)
    full_description = db.Column('full_description', db.String)
    logo = db.Column('logo', db.String)

    enabled = db.Column('enabled', db.Boolean)

    def update_candidate(self):
        candidate = Candidate.query.filter((Candidate.email == self.email) & (Candidate.ticker == self.ticker)).first()

        if candidate is None:
            db.session.add(self)
        else:
            candidate.ticker = self.ticker
            candidate.reason = self.reason
            candidate.enabled = self.enabled
            candidate.company_name = self.company_name
            candidate.exchange = self.exchange
            candidate.industry = self.industry
            candidate.sector = self.sector
            candidate.full_description = self.full_description
            candidate.logo = self.logo
        db.session.commit()

    def delete_candidate(self):
        db.session.delete(self)
        db.session.commit()

    def change_enabled_state(self):
        if self.enabled:
            self.enabled = False
        else:
            self.enabled = True
        db.session.commit()

    def to_dictionary(self):
        d = {}
        d['ticker'] = self.ticker
        d['description'] = self.reason
        return d
