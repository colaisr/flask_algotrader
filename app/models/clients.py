from .. import db


class Connection(db.Model):
    __tablename__ = 'Connections'
    # __bind_key__ = 'db_clients'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)
    reported_connection = db.Column('reported_connection', db.DateTime)

    def log_connection(self):
        db.session.add(self)
        db.session.commit()


class Report(db.Model):
    __tablename__ = 'Reports'
    # __bind_key__ = 'db_clients'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)
    report_time = db.Column('report_time', db.DateTime)
    net_liquidation = db.Column('net_liquidation', db.Float)
    remaining_sma_with_safety = db.Column('remaining_sma_with_safety', db.Float)
    excess_liquidity = db.Column('excess_liquidity', db.Float)
    remaining_trades = db.Column('remaining_trades', db.Integer)
    all_positions_value = db.Column('all_positions_value', db.Float)
    open_positions_json = db.Column('open_positions_json', db.String)
    open_orders_json = db.Column('open_orders_json', db.String)
    candidates_live_json = db.Column('candidates_live_json', db.String)
    dailyPnl = db.Column('dailyPnl', db.Float)
    last_worker_execution = db.Column('last_worker_execution', db.DateTime)
    market_time = db.Column('market_time', db.DateTime)
    started_time = db.Column('started_time', db.DateTime)
    market_state = db.Column('market_state', db.String)
    api_connected = db.Column('api_connected', db.Boolean)
    market_data_error = db.Column('market_data_error', db.Boolean)
    client_version = db.Column('client_version', db.String)

    def update_report(self):
        report = Report.query.filter_by(email=self.email).first()
        if report is None:
            db.session.add(self)
        else:
            report.report_time = self.report_time
            report.market_state = self.market_state
            report.started_time = self.started_time
            report.api_connected = self.api_connected
            if report.api_connected:
                report.net_liquidation = self.net_liquidation
                report.remaining_sma_with_safety = self.remaining_sma_with_safety
                report.excess_liquidity = self.excess_liquidity
                report.remaining_trades = self.remaining_trades
                report.all_positions_value = self.all_positions_value
                report.open_positions_json = self.open_positions_json
                report.open_orders_json = self.open_orders_json
                report.candidates_live_json = self.candidates_live_json
                report.dailyPnl = self.dailyPnl
                report.last_worker_execution = self.last_worker_execution
                report.market_time = self.market_time
                report.market_data_error = self.market_data_error
                report.client_version = self.client_version

        db.session.commit()


class ReportStatistic(db.Model):
    __tablename__ = 'ReportsStatistic'
    # __bind_key__ = 'db_clients'
    id = db.Column('id', db.Integer, primary_key=True)
    email = db.Column('email', db.String)
    report_time = db.Column('report_time', db.DateTime)
    net_liquidation = db.Column('net_liquidation', db.Float)
    remaining_sma_with_safety = db.Column('remaining_sma_with_safety', db.Float)
    excess_liquidity = db.Column('excess_liquidity', db.Float)
    remaining_trades = db.Column('remaining_trades', db.Integer)
    all_positions_value = db.Column('all_positions_value', db.Float)
    open_positions_json = db.Column('open_positions_json', db.String)
    open_orders_json = db.Column('open_orders_json', db.String)
    candidates_live_json = db.Column('candidates_live_json', db.String)
    dailyPnl = db.Column('dailyPnl', db.Float)
    last_worker_execution = db.Column('last_worker_execution', db.DateTime)
    market_time = db.Column('market_time', db.DateTime)
    started_time = db.Column('started_time', db.DateTime)
    market_state = db.Column('market_state', db.String)
    api_connected = db.Column('api_connected', db.Boolean)
    market_data_error = db.Column('market_data_error', db.Boolean)

    def add_report(self):
        db.session.add(self)
        db.session.commit()


# class JsonEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj.__class__, DeclarativeMeta):
#             # an SQLAlchemy class
#             fields = {}
#             for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
#                 data = obj.__getattribute__(field)
#                 if isinstance(data, (datetime, date)):
#                     data = datetime.isoformat(data)
#                 try:
#                     json.dumps(data)  # this will fail on non-encodable values, like other classes
#                     fields[field] = data
#                 except TypeError:
#                     fields[field] = None
#             # a json-encodable dict
#             return fields
#         return json.JSONEncoder.default(self, obj)
