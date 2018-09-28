# app/api/v1/resources/orders.py

from flask_restful import Resource, reqparse
import psycopg2

# local imports
from ..db import db


class Ordersv2(Resource):
    """post an order"""

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
        help="Quantity is required"
    )

    def get(self):
        """get all orders"""
        try:
            conn = db()
            cur = conn.cursor()
            cur.execute("SELECT * from orders WHERE user_id=%(id)s",
                        {'id': data["id"]})
            orders = cur.fetchall()

            return {"Message": orders}
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500

    def post(self):
        """create new order"""

        data = Ordersv2.parser.parse_args()
        item = data["item"]
        price = data["price"]
        quantity = data["quantity"]
        address = data["address"]

        if not item:
            return {'Message': 'Food item field is required'}, 400
        if not price:
            return {'Message': 'Price field is required'}, 400
        if not address:
            return {'Message': 'Address field is required'}, 400
        if not quantity:
            return {'Message': 'Quantity field is required'}, 400

        try:
            conn = db()
            cur = conn.cursor()

            cur.execute("SELECT * FROM orders WHERE food = %(food)s",
                        {'food': data['item']})

            # check if order exist
            if cur.fetchone() is not None:
                return {'Message': 'Order already exist'}
            cur.execute("INSERT INTO orders (food, price, address, quantity) VALUES (%(food)s, %(price)s, %(address)s, %(quantity)s);", {
                'food': data["item"], 'price': data["price"], 'address': data["address"], 'quantity': data['quantity']})
            conn.commit()
            return {'Message': 'Order created successfully'}, 201
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class EditOrder(Resource):
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
        help="Quantity is required"
    )

    def put(self, order_id):

        data = EditOrder.parser.parse_args()
        item = data["item"]
        price = data["price"]
        quantity = data["quantity"]
        address = data["address"]

        if not item:
            return {'Message': 'Food item field is required'}, 400
        elif not price:
            return {'Message': 'Price field is required'}, 400
        elif not quantity:
            return {'Message': 'Image field is required'}, 400
        elif not quantity:
            return {'Message': 'Image field is required'}, 400

        try:
            conn = db()
            cur = conn.cursor()

            cur.execute("SELECT * FROM orders WHERE order_id = %(order_id)s",
                        {'order_id': order_id})

            # check if order exist
            if cur.fetchone() is None:
                return {'Message': 'Invalid order id'}

            cur.execute("UPDATE  orders SET food=%s, price=%s, address= %s, quantity= %s WHERE order_id=%s",
                        (item, price, address, quantity, order_id))
            conn.commit()

            cur.execute("SELECT * FROM orders")
            res = cur.fetchone()
            return {'Order': res}
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
