from datetime import datetime, date
import json

from .. import db


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


class Strategy(db.Model):
    __tablename__ = 'Strategies'
    id = db.Column('id', db.Integer, primary_key=True)
    strategy = db.Column('strategy', db.String)


class UserStrategySettingsDefault(db.Model):
    __tablename__ = 'UserStrategySettingsDefault'
    id = db.Column('id', db.Integer, primary_key=True)
    strategy_id = db.Column('strategy_id', db.Integer)
    algo_min_rank = db.Column('algo_min_rank', db.Integer)
    algo_accepted_fmp_ratings = db.Column('algo_accepted_fmp_ratings', db.String)
    algo_max_yahoo_rank = db.Column('algo_max_yahoo_rank', db.Float)
    algo_min_underprice = db.Column('algo_min_underprice', db.Float)
    algo_min_momentum = db.Column('algo_min_momentum', db.Float)
    algo_min_stock_invest_rank = db.Column('algo_min_stock_invest_rank', db.Float)
    algo_apply_min_rank = db.Column('algo_apply_min_rank', db.Boolean)
    algo_apply_accepted_fmp_ratings = db.Column('algo_apply_accepted_fmp_ratings', db.Boolean)
    algo_apply_max_yahoo_rank = db.Column('algo_apply_max_yahoo_rank', db.Boolean)
    algo_apply_min_stock_invest_rank = db.Column('algo_apply_min_stock_invest_rank', db.Boolean)
    algo_apply_min_underprice = db.Column('algo_apply_min_underprice', db.Boolean)
    algo_apply_min_momentum = db.Column('algo_apply_min_momentum', db.Boolean)
    algo_min_beta = db.Column('algo_min_beta', db.Float)
    algo_apply_min_beta = db.Column('algo_apply_min_beta', db.Boolean)
    algo_max_intraday_drop_percent = db.Column('algo_max_intraday_drop_percent', db.Float)
    algo_apply_max_intraday_drop_percent = db.Column('algo_apply_max_intraday_drop_percent', db.Boolean)
    algo_apply_algotrader_rank = db.Column('algo_apply_algotrader_rank', db.Boolean)
    algo_min_algotrader_rank = db.Column('algo_min_algotrader_rank', db.Float)


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
    algo_allow_sell = db.Column('algo_allow_sell', db.Boolean)
    algo_allow_margin = db.Column('algo_allow_margin', db.Boolean)
    algo_portfolio_stoploss = db.Column('algo_portfolio_stoploss', db.Integer)
    algo_apply_min_rank = db.Column('algo_apply_min_rank', db.Boolean)
    algo_min_rank = db.Column('algo_min_rank', db.Integer)
    algo_apply_accepted_fmp_ratings = db.Column('algo_apply_accepted_fmp_ratings', db.Boolean)
    algo_accepted_fmp_ratings = db.Column('algo_accepted_fmp_ratings', db.String)
    algo_sell_on_swan = db.Column('algo_sell_on_swan', db.Boolean)
    algo_positions_for_swan = db.Column('algo_positions_for_swan', db.Float)
    algo_apply_max_yahoo_rank = db.Column('algo_apply_max_yahoo_rank', db.Boolean)
    algo_max_yahoo_rank = db.Column('algo_max_yahoo_rank', db.Float)
    algo_apply_max_hold = db.Column('algo_apply_max_hold', db.Boolean)
    algo_max_hold_days = db.Column('algo_max_hold_days', db.Integer)
    algo_apply_min_underprice = db.Column('algo_apply_min_underprice', db.Boolean)
    algo_min_underprice = db.Column('algo_min_underprice', db.Float)
    algo_apply_min_momentum = db.Column('algo_apply_min_momentum', db.Boolean)
    algo_min_momentum = db.Column('algo_min_momentum', db.Float)
    algo_apply_min_stock_invest_rank = db.Column('algo_apply_min_stock_invest_rank', db.Boolean)
    algo_min_stock_invest_rank = db.Column('algo_min_stock_invest_rank', db.Float)
    connection_account_name = db.Column('connection_account_name', db.String)
    connection_port = db.Column('connection_port', db.Integer)
    connection_tws_user = db.Column('connection_tws_user', db.String)
    connection_tws_pass = db.Column('connection_tws_pass', db.String)
    station_interval_ui_sec = db.Column('station_interval_ui_sec', db.Integer)
    station_interval_worker_sec = db.Column('station_interval_worker_sec', db.Integer)
    station_autorestart = db.Column('station_autorestart', db.Boolean)
    server_url = db.Column('server_url', db.String)
    server_report_interval_sec = db.Column('server_report_interval_sec', db.Integer)
    server_use_system_candidates = db.Column('server_use_system_candidates', db.Boolean)
    notify_buy = db.Column('notify_buy', db.Boolean)
    notify_sell = db.Column('notify_sell', db.Boolean)
    notify_trail = db.Column('notify_trail', db.Boolean)
    algo_min_beta = db.Column('algo_min_beta', db.Float)
    algo_apply_min_beta = db.Column('algo_apply_min_beta', db.Boolean)
    algo_max_intraday_drop_percent = db.Column('algo_max_intraday_drop_percent', db.Float)
    algo_apply_max_intraday_drop_percent = db.Column('algo_apply_max_intraday_drop_percent', db.Boolean)
    strategy_id = db.Column('strategy_id', db.Integer)
    algo_apply_algotrader_rank = db.Column('algo_apply_algotrader_rank', db.Boolean)
    algo_min_algotrader_rank = db.Column('algo_min_algotrader_rank', db.Float)

    def __init__(self, email, **kwargs):
        super(UserSetting, self).__init__(**kwargs)
        # self.strategy = Strategy.query.filter_by(strategy_id=self.strategy_id).first().strategy
        self.email = email
        self.algo_max_loss = -10
        self.algo_take_profit = 6
        self.algo_bulk_amount_usd = 1000
        self.algo_trailing_percent = 1
        self.algo_allow_buy = False
        self.algo_allow_sell = False
        self.algo_allow_margin = True
        self.algo_portfolio_stoploss = 0
        self.algo_sell_on_swan = True
        self.algo_positions_for_swan = -3
        self.algo_apply_max_hold = True
        self.algo_max_hold_days = 31
        self.connection_account_name = 'U0000000'
        self.connection_port = 7498
        self.connection_tws_user = 'your_tws_user_name'
        self.connection_tws_pass = 'your_tws_user_password'
        self.station_interval_ui_sec = 1
        self.station_interval_worker_sec = 60
        self.station_autorestart = True
        self.server_url = 'https://www.algotrader.company'
        self.server_report_interval_sec = 30
        self.server_use_system_candidates = True
        self.notify_buy = True
        self.notify_sell = True
        self.notify_trail = True
        self.strategy_id = 1
        self.get_strategy_default(self.strategy_id)

    def get_strategy_default(self, strategy_id):
        strategy = UserStrategySettingsDefault.query.filter_by(id=strategy_id).first()
        self.algo_min_rank = strategy.algo_min_rank
        self.algo_accepted_fmp_ratings = strategy.algo_accepted_fmp_ratings
        self.algo_max_yahoo_rank = strategy.algo_max_yahoo_rank
        self.algo_min_stock_invest_rank = strategy.algo_min_stock_invest_rank
        self.algo_min_underprice = strategy.algo_min_underprice
        self.algo_min_momentum = strategy.algo_min_momentum
        self.algo_apply_min_rank = strategy.algo_apply_min_rank
        self.algo_apply_accepted_fmp_ratings = strategy.algo_apply_accepted_fmp_ratings
        self.algo_apply_max_yahoo_rank = strategy.algo_apply_max_yahoo_rank
        self.algo_apply_min_stock_invest_rank = strategy.algo_apply_min_stock_invest_rank
        self.algo_apply_min_underprice = strategy.algo_apply_min_underprice
        self.algo_apply_min_momentum = strategy.algo_apply_min_momentum
        self.algo_min_beta = strategy.algo_min_beta
        self.algo_apply_min_beta = strategy.algo_apply_min_beta
        self.algo_max_intraday_drop_percent = strategy.algo_max_intraday_drop_percent
        self.algo_apply_max_intraday_drop_percent = strategy.algo_apply_max_intraday_drop_percent
        self.algo_apply_algotrader_rank = strategy.algo_apply_algotrader_rank
        self.algo_min_algotrader_rank = strategy.algo_min_algotrader_rank

    def update_user_settings(self):
        settings = UserSetting.query.filter((UserSetting.email == self.email)).first()

        if settings is None:
            db.session.add(self)

        db.session.commit()

    def toJson(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def toDictionary(self):
        d = {}
        d['email'] = self.email
        d['algo_max_loss'] = self.algo_max_loss
        d['algo_take_profit'] = self.algo_take_profit
        d['algo_bulk_amount_usd'] = self.algo_bulk_amount_usd
        d['algo_trailing_percent'] = self.algo_trailing_percent
        d['connection_port'] = self.connection_port
        d['connection_account_name'] = self.connection_account_name
        d['connection_tws_user'] = self.connection_tws_user
        d['connection_tws_pass'] = self.connection_tws_pass
        d['server_url'] = self.server_url
        d['server_report_interval_sec'] = self.server_report_interval_sec
        d['server_use_system_candidates'] = self.server_use_system_candidates
        d['station_interval_worker_sec'] = self.station_interval_worker_sec
        d['station_interval_ui_sec'] = self.station_interval_ui_sec
        d['station_autorestart'] = self.station_autorestart
        d['algo_allow_buy'] = self.algo_allow_buy
        d['algo_allow_sell'] = self.algo_allow_sell
        d['algo_allow_margin'] = self.algo_allow_margin
        d['algo_portfolio_stoploss'] = self.algo_portfolio_stoploss
        d['algo_min_rank'] = self.algo_min_rank
        d['algo_accepted_fmp_ratings'] = self.algo_accepted_fmp_ratings
        d['algo_apply_min_rank'] = self.algo_apply_min_rank
        d['algo_apply_accepted_fmp_ratings'] = self.algo_apply_accepted_fmp_ratings
        d['algo_sell_on_swan'] = self.algo_sell_on_swan
        d['algo_positions_for_swan'] = self.algo_positions_for_swan
        d['algo_apply_max_yahoo_rank'] = self.algo_apply_max_yahoo_rank
        d['algo_max_yahoo_rank'] = self.algo_max_yahoo_rank
        d['algo_apply_max_hold'] = self.algo_apply_max_hold
        d['algo_max_hold_days'] = self.algo_max_hold_days
        d['algo_apply_min_underprice'] = self.algo_apply_min_underprice
        d['algo_min_underprice'] = self.algo_min_underprice
        d['algo_apply_min_momentum'] = self.algo_apply_min_momentum
        d['algo_min_momentum'] = self.algo_min_momentum
        d['notify_buy'] = self.notify_buy
        d['notify_sell'] = self.notify_sell
        d['notify_trail'] = self.notify_trail
        d['strategy_id'] = self.strategy_id
        d['algo_apply_algotrader_rank'] = self.algo_apply_algotrader_rank
        d['algo_min_algotrader_rank'] = self.algo_min_algotrader_rank
        return d
