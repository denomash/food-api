# app/api/v1/resources/orders.py

from flask_restful import Resource, reqparse
import psycopg2
import psycopg2.extras

# local imports
from ..db import db
from ..checkauth import check_auth


class Ordersv2(Resource):

    @check_auth
    def get(current_user, self):
        """get all orders"""

        if current_user["type"] != "admin":
            return {"Message": "Must be an admin"}
        try:
            conn = db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * from orders")
            orders = cur.fetchall()

            return {"Message": orders}
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class EditOrderv2(Resource):
    """docstring for Orders"""

    @check_auth
    def put(current_user, self, order_id):
        """update order by id by admin"""
        if current_user["type"] != "admin":
            return {"Message": "Must be an admin"}

        parser = reqparse.RequestParser()

        parser.add_argument(
            'status',
            type=str,
            required=True,
            help="Status is required"
        )

        data = parser.parse_args()
        status = data["status"]

        if not status:
            return {'Message': 'Status can\'t be empty'}, 400
        elif status not in ('pending', 'completed'):
            return {'Message': 'Status must be either pending or completed'}, 400

        try:
            conn = db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("SELECT * FROM orders WHERE order_id = %(order_id)s",
                        {'order_id': order_id})

            # check if order exist
            if cur.fetchone() is None:
                return {'Message': 'Invalid order id'}

            cur.execute("UPDATE  orders SET status=%s WHERE order_id=%s",
                        (status, order_id))
            conn.commit()
            res = cur.fetchone()

            return {'Message': res}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500

    @check_auth
    def get(current_user, self, order_id):
        """get order by id by admin"""
        if current_user["type"] != "admin":
            return {"Message": "Must be an admin"}, 401

        try:
            conn = db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("SELECT * FROM orders WHERE order_id = %(order_id)s",
                        {'order_id': order_id})

            # check if order exist
            res = cur.fetchone()
            if res is None:
                return {'Message': 'Invalid order id'}

            return {'Message': res}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class UserOrder(Resource):
    """docstring for Orders"""

    @check_auth
    def post(current_user, self):
        """user can order food"""
        parser = reqparse.RequestParser()

        parser.add_argument(
            'mealId',
            type=int,
            required=True,
            help="mealId is required"
        )
        parser.add_argument(
            'quantity',
            type=int,
            required=True,
            help="Quantity is required"
        )
        parser.add_argument(
            'address',
            type=str,
            required=True,
            help="Address is required"
        )

        data = parser.parse_args()
        meal_id = data["mealId"]
        quantity = data["quantity"]
        address = data["address"]
        status = 'pending'
        user_id = current_user["id"]

        if not item:
            return {'Message': 'Food item field is required'}, 400
        if not address:
            return {'Message': 'Address field is required'}, 400
        if not quantity:
            return {'Message': 'Quantity field is required'}, 400

        try:
            conn = db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("SELECT * FROM orders WHERE food = %(food)s",
                        {'food': data['item']})

            # check if order exist
            res = cur.fetchone()
            if res is not None:
                return {'Message': 'Order already exist'}

            cur.execute("INSERT INTO orders (meal_id, address, quantity, status) VALUES (%(meal_id)s, %(quantity)s, %(address)s, %(status)s);", {
                'meal_id': meal_id, 'address': address, 'quantity': quantity, 'status': status})
            conn.commit()
            return {'Message': res}, 201
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500

    @check_auth
    def get(current_user, self):
        """user can get order history"""

        try:
            conn = db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("SELECT * FROM orders WHERE user_id = %(user_id)s",
                        {'user_id': current_user['id']})
            print(current_user['id'])

            # check if order exist
            res = cur.fetchall()
            if not res:
                return {'Message': 'No order history'}, 404

            return {'Message': res}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
