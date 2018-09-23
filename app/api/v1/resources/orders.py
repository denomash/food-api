# app/api/v1/resources/orders.py

from flask_restful import Resource

# local imports
from ..models import order_data


class Orders(Resource):
    """docstring for Orders"""

    def get(self):
        """get all orders"""
        if not order_data:

            return {'Message': 'No orders found'}, 404
        else:

            return {'Orders': order_data}, 200
