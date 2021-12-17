from datetime import datetime

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
    exchange_short = db.Column('exchange_short', db.String)
    industry = db.Column('industry', db.String)
    sector = db.Column('sector', db.String)
    full_description = db.Column('full_description', db.String)
    logo = db.Column('logo', db.String)
    website = db.Column('website', db.String)
    isActivelyTrading_fmp = db.Column('isActivelyTrading_fmp', db.Boolean)
    added_at = db.Column('added_at', db.DateTime)
    price_added = db.Column('price_added', db.Float)

    enabled = db.Column('enabled', db.Boolean)

    def update_candidate(self):
        candidate = Candidate.query.filter((Candidate.email == self.email) & (Candidate.ticker == self.ticker)).first()

        if candidate is None:
            self.added_at = datetime.utcnow()
            db.session.add(self)
        else:
            candidate.ticker = self.ticker
            candidate.reason = self.reason
            candidate.enabled = self.enabled
            candidate.isActivelyTrading_fmp = self.isActivelyTrading_fmp
            candidate.company_name = self.company_name
            candidate.exchange = self.exchange
            candidate.exchange_short = self.exchange_short
            candidate.industry = self.industry
            candidate.sector = self.sector
            candidate.full_description = self.full_description
            candidate.logo = self.logo
            candidate.website = self.website
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
        d['company_name'] = self.company_name
        d['logo'] = self.logo
        d['added_at'] = self.added_at
        d['price_added'] = self.price_added
        return d
