# app/api/v1/resources/orders.py

from flask_restful import Resource, reqparse

# local imports
from ..models import order_data


class Get_orders(Resource):
    """docstring for Order"""

    def get(self):
        """get all orders"""
        if not order_data:
            return {'Message': 'No orders found'}, 404
        else:
            return {'Orders': order_data}, 200


class Orders(Resource):
    """docstring for Orders"""

    parser = reqparse.RequestParser()

    parser.add_argument(
        'item',
        type=str,
        required=True,
        help="Food item is required"
    )
    parser.add_argument(
        'price',
        type=float,
        required=True,
        help="Price is required"
    )
    parser.add_argument(
        'address',
        type=str,
        required=True,
        help="Price is required"
    )
    parser.add_argument(
        'quantity',
        type=int,
        required=True,
        help="Number of food items is required"
    )

    def post(self):
        """create new order"""

        data = Orders.parser.parse_args()

        exist = [order for order in order_data if order['item'] == data['item']]

        if (len(exist) != 0):

            return {'Message': 'Ordered item alredy exist'}, 400

        id = len(order_data) + 1

        new_order = {
            'id': id,
            'item': data['item'],
            'price': data['price'],
            'quantity': data['quantity'],
            'address': data['address'],
            'delivered': False
        }

        order_data.append(new_order)

        return {'Order': new_order}, 201


class Orderbyid(Resource):
    """docstring for Orders by id """

    def get(self, order_id):
        """ get order by id"""

        exist = [order for order in order_data if order['id'] == order_id]

        if not exist:

            return {'Message': 'Invalid order id'}, 400

        else:

            return {'Order': exist[0]}, 200
