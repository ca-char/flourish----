from dotenv import load_dotenv
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import Flask
from config import Config
from web_app.extensions import db, login_manager, csrf, limiter, bcrypt
from web_app.models import User
from web_app.routes.views import views
from web_app.routes.auth import auth
from web_app.db_management import create_db, insert_sample_data

load_dotenv()
print(os.getenv("SECRET_KEY"))

def configure_logging(app): 
    LOG_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "logs")
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)

    file_handler = RotatingFileHandler(
            "logs/app.log",
            maxBytes=1_000_000,
            backupCount=5
        )
    file_handler.setLevel(logging.WARNING)
    formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
    )
    file_handler.setFormatter(formatter)

    logging.getLogger().addHandler(file_handler)
    logging.getLogger().setLevel(logging.WARNING)


def create_app(config_overrides=None, test_config=None):
    app = Flask(__name__, static_folder='static')

    app.config.from_object(Config)

    if config_overrides:
        app.config.update(config_overrides)

    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    limiter.init_app(app)
    bcrypt.init_app(app)
    configure_logging(app)

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        create_db(reset=False)

        if app.config.get("LOAD_SAMPLE_DATA"):
            if User.query.count() == 0:
                insert_sample_data()
                
        if not test_config:
            if User.query.count() == 0:
                insert_sample_data()

    return app
