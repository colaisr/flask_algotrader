from datetime import datetime,date
import json

from .. import db

def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))

class UserSetting(db.Model):
    __tablename__ = 'UserSettings'
    # __bind_key__ = 'db_clients'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)

    algo_take_profit = db.Column('algo_take_profit', db.Integer)
    algo_max_loss = db.Column('algo_max_loss', db.Integer)
    algo_trailing_percent = db.Column('algo_trailing_percent', db.Integer)
    algo_bulk_amount_usd = db.Column('algo_bulk_amount_usd', db.Integer)
    algo_allow_buy = db.Column('algo_allow_buy', db.Boolean)
    algo_allow_margin = db.Column('algo_allow_margin', db.Boolean)


    connection_account_name = db.Column('connection_account_name', db.String)
    connection_port = db.Column('connection_port', db.Integer)
    connection_tws_user = db.Column('connection_tws_user', db.String)
    connection_tws_pass = db.Column('connection_tws_pass', db.String)

    station_interval_ui_sec = db.Column('station_interval_ui_sec', db.Integer)
    station_interval_worker_sec = db.Column('station_interval_worker_sec', db.Integer)

    server_url = db.Column('server_url', db.String)
    server_report_interval_sec = db.Column('server_report_interval_sec', db.Integer)
    server_use_system_candidates = db.Column('server_use_system_candidates', db.Boolean)

    def update_user_settings(self):
        settings = UserSetting.query.filter((UserSetting.email==self.email)).first()

        if settings is None:
            db.session.add(self)

        db.session.commit()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def toDictionary(self):
        d={}
        d['email']=self.email
        d['algo_max_loss']=self.algo_max_loss
        d['algo_take_profit']=self.algo_take_profit
        d['algo_bulk_amount_usd']=self.algo_bulk_amount_usd
        d['algo_trailing_percent']=self.algo_trailing_percent
        d['connection_port']=self.connection_port
        d['connection_account_name']=self.connection_account_name
        d['connection_tws_user'] = self.connection_tws_user
        d['connection_tws_pass'] = self.connection_tws_pass
        d['server_url']=self.server_url
        d['server_report_interval_sec']=self.server_report_interval_sec
        d['server_use_system_candidates'] = self.server_use_system_candidates
        d['station_interval_worker_sec']=self.station_interval_worker_sec
        d['station_interval_ui_sec']=self.station_interval_ui_sec
        d['algo_allow_buy'] = self.algo_allow_buy
        d['algo_allow_margin'] = self.algo_allow_margin

        return d