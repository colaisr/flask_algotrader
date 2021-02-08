from .. import db


class Connection(db.Model):
    __tablename__ = 'Connections'
    __bind_key__ = 'db_clients'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100))
    reported_connection = db.Column(db.DateTime)

    def log_connection(self):
        db.session.add(self)
        db.session.commit()
