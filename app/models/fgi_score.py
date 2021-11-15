from .. import db


class Fgi_score(db.Model):
    __tablename__ = 'Fgi_Scores'
    id = db.Column('id', db.Integer, primary_key=True)
    score_time = db.Column('score_time', db.DateTime)
    fgi_value = db.Column('fgi_value', db.Integer)
    fgi_text = db.Column('fgi_text', db.String)
    updated_cnn = db.Column('updated_cnn', db.String)


    def add_score(self):
        db.session.add(self)
        db.session.commit()

