from .. import db


class Tooltip(db.Model):
    __tablename__ = 'Tooltips'
    id = db.Column('id', db.Integer, primary_key=True)
    short_name = db.Column('short_name', db.String)
    title = db.Column('title', db.String)
    content = db.Column('content', db.String)
    url = db.Column('url', db.String)

