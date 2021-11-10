from .. import db


class User_login(db.Model):
    __tablename__ = 'UserLogins'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)
    user_ip = db.Column('user_ip', db.String)
    browser = db.Column('browser', db.String)
    useragent_string = db.Column('useragent_string', db.String)
    login_time_utc = db.Column('login_time_utc', db.DateTime)

    def add_login(self):
        db.session.add(self)
        db.session.commit()

