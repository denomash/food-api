# app/__init__.py

from flask import Flask, Blueprint, render_template
from flask_restful import Api
from flask import redirect

# local imports
from config import configuration
from .api.v1.resources.orders import Get_orders, Orders, Orderbyid
from .api.v1.resources.auth import Register, Login
from .api.v2.db import init_db
from .api.v2.resources.orders import Ordersv2, EditOrderv2, UserOrder
from .api.v2.resources.auth import Registerv2, LoginV2
from .api.v2.resources.food import Menu
from .api.v2.resources.promote import Promote
from .api.v2.resources.users import Users

# Inisialize blueprint and flask-restful
api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)


def create_app(configuration_name):
    """Initialize the app"""

    app = Flask(__name__, instance_relative_config=True)

    # Load the config file
    app.config.from_object(configuration[configuration_name])

    # initialize database
    with app.app_context():
        init_db()

    # register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # base route
    @app.route('/')
    def index():
        """base route"""
        return redirect("/apidocs")

    return app

# Resourses
api.add_resource(Get_orders, '/v1/orders')
api.add_resource(Orders, '/v1/orders')
api.add_resource(Orderbyid, '/v1/orders/<int:order_id>')
api.add_resource(Register, '/v1/signup')
api.add_resource(Login, '/v1/login')
api.add_resource(Ordersv2, '/v2/orders')
api.add_resource(EditOrderv2, '/v2/orders/<int:order_id>')
api.add_resource(Registerv2, '/v2/auth/signup')
api.add_resource(LoginV2, '/v2/auth/login')
api.add_resource(Menu, '/v2/menu')
api.add_resource(UserOrder, '/v2/users/orders')
api.add_resource(Promote, '/v2/promote/<int:user_id>')
api.add_resource(Users, '/v2/users')
