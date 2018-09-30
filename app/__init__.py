# app/__init__.py

from flask import Flask, Blueprint, render_template
from flask_restful import Api

# local imports
from config import configuration
from .api.v2.db import init_db
from .api.v1.resources.orders import Get_orders, Orders, Orderbyid
from .api.v1.resources.auth import Register, Login
from .api.v2.resources.orders import Ordersv2, EditOrder
from .api.v2.resources.auth import Registerv2, LoginV2

# Inisialize blueprint and flask-restful
api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


def create_app(configuration_name):
    """Initialize the app"""

    app = Flask(__name__, instance_relative_config=True)

    # Load the config file
    app.config.from_object(configuration[configuration_name])

    # initialize database
    init_db()

    # register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # base route
    @app.route('/')
    def index():
        """base route"""
        return render_template('index.html')

    return app

# Resourses
api.add_resource(Get_orders, '/v1/orders')
api.add_resource(Orders, '/v1/orders')
api.add_resource(Orderbyid, '/v1/orders/<int:order_id>')
api.add_resource(Register, '/v1/signup')
api.add_resource(Login, '/v1/login')
api.add_resource(Ordersv2, '/v2/orders')
api.add_resource(EditOrder, '/v1/orders/<int:order_id>')
api.add_resource(Registerv2, '/auth/signup')
api.add_resource(LoginV2, '/auth/login')
