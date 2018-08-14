from flask import Flask

from app import commands
from app.commands import asd
from app.views import application


def create_app():
    # create and configure the application
    app = Flask(__name__, instance_relative_config=True)

    _load_config(app)
    _register_blueprints(app)
    _register_cli(app)

    return app


def _load_config(app):
    app.config.from_pyfile('config.cfg')


def _register_blueprints(app):
    app.register_blueprint(application)


def _register_cli(app):
    app.cli.add_command(asd)
