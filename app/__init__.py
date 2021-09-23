import os

from flask import Flask
from flask_assets import Environment
from flask_compress import Compress
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_rq import RQ
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

from app.assets import app_css, app_js, vendor_css, vendor_js
from config import config as Config

basedir = os.path.abspath(os.path.dirname(__file__))

mail = Mail()
db = SQLAlchemy()
csrf = CSRFProtect()
compress = Compress()
migrate = Migrate()

# Set up Flask-Login
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'account.login'


def create_app(config):
    app = Flask(__name__)
    config_name = config

    if not isinstance(config, str):
        config_name = os.getenv('FLASK_CONFIG', 'default')

    app.config.from_object(Config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # not using sqlalchemy event system, hence disabling it

    Config[config_name].init_app(app)
    # migrate.init_app(app, db)

    # Set up extensions
    mail.init_app(app)
    if 'colakamornik' in app.static_folder or 'lilia' in app.static_folder:    #means running on local machine
        import sshtunnel
        ssh_url = os.getenv('SSH_URL', 'default')
        ssh_user = os.getenv('SSH_USER', 'default')
        ssh_password = os.getenv('SSH_PASSWORD', 'default')
        mysql_user = os.getenv('MYSQL_USER', 'default')
        mysql_password = os.getenv('MYSQL_PASSWORD', 'default')
        sql_name = 'colak$algotrader' if 'colakamornik' in app.static_folder else 'colak$algotrader_test'

        tunnel = sshtunnel.SSHTunnelForwarder(
            (ssh_url), ssh_username=ssh_user, ssh_password=ssh_password,
            remote_bind_address=('colak.mysql.eu.pythonanywhere-services.com', 3306)
        )

        tunnel.start()
        app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+pymysql://{mysql_user}:{mysql_password}@127.0.0.1:{tunnel.local_bind_port}/{sql_name}'

    app.config['SQLALCHEMY_POOL_RECYCLE'] = 280
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    compress.init_app(app)
    RQ(app)

    # Register Jinja template functions
    from .utils import register_template_utils
    register_template_utils(app)

    # Set up asset pipeline
    # assets_env = Environment(app)
    # dirs = ['assets/styles', 'assets/scripts']
    # for path in dirs:
    #     assets_env.append_path(os.path.join(basedir, path))
    # assets_env.url_expire = True
    #
    # assets_env.register('app_css', app_css)
    # assets_env.register('app_js', app_js)
    # assets_env.register('vendor_css', vendor_css)
    # assets_env.register('vendor_js', vendor_js)

    # app.static_folder = 'static'
    # Configure SSL if platform supports it
    if not app.debug and not app.testing and not app.config['SSL_DISABLE']:
        from flask_sslify import SSLify
        SSLify(app)

    # Create app blueprints
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .account import account as account_blueprint
    app.register_blueprint(account_blueprint, url_prefix='/account')

    from .userview import userview as userview_blueprint
    app.register_blueprint(userview_blueprint, url_prefix='/userview')

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .connections import connections as connections_blueprint
    app.register_blueprint(connections_blueprint, url_prefix='/connections')

    from .market_data import marketdata as marketdata_blueprint
    app.register_blueprint(marketdata_blueprint, url_prefix='/marketdata')

    from .algotrader_settings import algotradersettings as algotradersettings_blueprint
    app.register_blueprint(algotradersettings_blueprint, url_prefix='/algotradersettings')

    from .closed_position_info import closed_position_info as closed_position_info_blueprint
    app.register_blueprint(closed_position_info_blueprint, url_prefix='/closed_position_info')

    from .station import station as station_blueprint
    app.register_blueprint(station_blueprint, url_prefix='/station')

    from .research import research as research_blueprint
    app.register_blueprint(research_blueprint, url_prefix='/research')

    from .candidates import candidates as candidates_blueprint
    app.register_blueprint(candidates_blueprint, url_prefix='/candidates')

    from .test import test as test_blueprint
    app.register_blueprint(test_blueprint, url_prefix='/test')

    return app


