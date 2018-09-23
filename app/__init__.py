# app/__init__.py

from flask import Flask

# local imports
from config import configuration



def create_app(configuration_name):

    app = Flask(__name__, instance_relative_config=True)

    # Load the config file

    app.config.from_object(configuration[configuration_name])

    # base route
    @app.route('/')
    def index():
        """base route"""
        return "Hello champ!!"
    

    return app

