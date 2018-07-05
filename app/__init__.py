from flask import Flask, Blueprint
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from . import views, errors

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
main = Blueprint('main', __name__)


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    bootstrap.init_app(app)
    mail.init_app(app)
    mail.init_app(app)
    moment.init_app(app)
    db.init_app(app)

    return app
