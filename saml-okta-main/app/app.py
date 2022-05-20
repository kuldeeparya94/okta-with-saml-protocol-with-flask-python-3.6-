# -*- coding: utf-8 -*-

"""The app module, containing the app factory function."""
import os
import logging.config

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from app import home, user
from app.user.views import User

login_manager = LoginManager()


def create_app(config=None):
    configure_log()

    app = Flask(__name__.split('.')[0])
    app.config.from_object(config)

    Bootstrap(app)
    login_manager.init_app(app)

    register_blueprints(app)
    return app


def register_blueprints(app):
    app.register_blueprint(home.views.blueprint)
    app.register_blueprint(user.views.blueprint)


def configure_log():
    logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
    logging.config.fileConfig(logging_conf_path)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)
