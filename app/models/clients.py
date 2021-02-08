from .. import db


class Connection(db.Model):
    __tablename__ = 'Connections'
    __bind_key__ = 'db_clients'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)
    reported_connection = db.Column('reported_connection', db.DateTime)

    def log_connection(self):
        db.session.add(self)
        db.session.commit()


class Report(db.Model):
    __tablename__ = 'Reports'
    __bind_key__ = 'db_clients'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)
    report_time = db.Column('report_time', db.DateTime)
    net_liquidation = db.Column('net_liquidation', db.Float)
    remaining_sma_with_safety = db.Column('remaining_sma_with_safety', db.Float)
    remaining_trades = db.Column('remaining_trades', db.Integer)
    all_positions_value = db.Column('all_positions_value', db.Float)
    open_positions_json = db.Column('open_positions_json', db.String)
    open_orders_json = db.Column('open_orders_json', db.String)
    dailyPnl=db.Column('dailyPnl', db.Float)

    def log_report(self):
        db.session.add(self)
        db.session.commit()
