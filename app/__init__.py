# app/__init__.py

from flask import Flask, Blueprint
from flask_restful import Api

# local imports
from config import configuration
from .api.v1.db import init_db
from .api.v1.resources.orders import Get_orders, Orders, Orderbyid
from .api.v1.resources.auth import Register, Login

# Inisialize blueprint and flask-restful
api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


def create_app(configuration_name):
    """Initialize the app"""

    app = Flask(__name__, instance_relative_config=True)

    # Load the config file
    app.config.from_object(configuration[configuration_name])

    # initialize the database
    init_db()

    # register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app

# Resourses
api.add_resource(Get_orders, '/orders')
api.add_resource(Orders, '/orders')
api.add_resource(Orderbyid, '/orders/<int:order_id>')
api.add_resource(Register, '/signup')
api.add_resource(Login, '/login')
