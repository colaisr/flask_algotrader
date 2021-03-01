from .. import db

class RestartRequest(db.Model):
    __tablename__ = 'RestartRequests'
    __bind_key__ = 'db_clients'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)


    def log_request(self):
        db.session.add(self)
        db.session.commit()

    def remove_request(self):
        db.session.delete(self)
        db.session.commit()