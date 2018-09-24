# app/api/v1/resources/orders.py

from flask_restful import Resource, reqparse

# local imports
from ..models import order_data, get_by_id, is_empty


class Get_orders(Resource):
    """docstring for Order"""

    def get(self):
        """get all orders"""
        if is_empty(order_data):
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
        help="Address is required"
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

            return {'Message': 'Ordered item already exist'}, 400

        _id = len(order_data) + 1

        new_order = {
            'id': _id,
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

    parser = reqparse.RequestParser()

    parser.add_argument(
        'item',
        type=str
    )
    parser.add_argument(
        'price',
        type=float
    )
    parser.add_argument(
        'address',
        type=str,
        required=True,
        help="Price is required"
    )
    parser.add_argument(
        'quantity',
        type=int
    )

    def get(self, order_id):
        """ get order by id"""

        exist = get_by_id(order_id)

        if not exist:

            return {'Message': 'Invalid order id'}, 400

        else:

            return {'Order': exist}, 200

    def put(self, order_id):
        """update order by id"""

        data = Orderbyid.parser.parse_args()
        exist = get_by_id(order_id)

        if not exist:

            return {'Message': 'Invalid order id'}, 400
        else:
            for order in order_data:
                if (order_id == order['id']):
                    order['item'] = data['item']
                    order['price'] = data['price']
                    order['quantity'] = data['quantity']
                    order['address'] = data['address']
                    return order, 200

    def delete(self, order_id):
        """ delete an order """

        order_to_delete = get_by_id(order_id)

        if not order_to_delete:

            return {'Message': 'Invalid order id'}, 404

        else:

            order_data.remove(order_to_delete[0])
            return {'Order': 'Order deleted'}, 200
