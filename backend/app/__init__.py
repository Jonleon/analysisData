import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_caching import Cache
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from config import Config


db = SQLAlchemy()
migrate = Migrate()
# login = LoginManager()
# login.login_view = 'auth.login'



cache = Cache(config={'CACHE_TYPE': 'simple'})



def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)
    db.init_app(app)
    migrate.init_app(app,db)
    # login.init_app(app)
    cache.init_app(app)
    from app.errors import bp as errors_bp
    app.register_blueprint(errors_bp)

    from app.core import bp as core_bp
    app.register_blueprint(core_bp)

    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/flaskapp.log',
                                           maxBytes=10240,
                                           backupCount=10)
        file_handler.setFormatter(
            logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
            ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.setLevel(logging.INFO)
        app.logger.info('start')
    return app
from app import models
