from flask import Flask

from app import commands
from app.commands import asd
from app.views import application


def create_app():
    # create and configure the application
    app = Flask(__name__)

    _register_cli(app)
    _register_blueprints(app)

    return app

def _register_blueprints(app):
    app.register_blueprint(application)

def _register_cli(app):
    app.cli.add_command(commands.asd)