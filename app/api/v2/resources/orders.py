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
            return {"Message": "Must be an admin"}, 401
        try:
            conn = db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * from orders")
            orders = cur.fetchall()

            if not orders:
                return {"Message": "No orders found"}, 404

            return {"Message": orders}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            conn = db()
            cur = conn.cursor()
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class EditOrderv2(Resource):
    """docstring for Orders"""

    @check_auth
    def put(current_user, self, order_id):
        """update order by id by admin"""
        if current_user["type"] != "admin":
            return {"Message": "Must be an admin"}, 401

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
        elif status not in ('New', 'Processing', 'Cancelled', 'Complete'):
            return {'Message': 'Status must be either  New, Processing, Cancelled or Complete'}, 400

        try:
            conn = db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("SELECT * FROM orders WHERE order_id = %(order_id)s",
                        {'order_id': order_id})

            # check if order exist
            res = cur.fetchone()
            if res is None:
                return {'Message': 'Invalid order id'}, 400

            cur.execute("UPDATE  orders SET status=%(status)s WHERE order_id=%(order_id)s",
                        {'status': status, 'order_id': order_id})
            conn.commit()

            return {'Message': 'Order status updated'}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            conn = db()
            cur = conn.cursor()
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
                return {'Message': 'Invalid order id'}, 400

            return {'Message': res}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            conn = db()
            cur = conn.cursor()
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
        status = 'New'
        user_id = current_user["id"]

        if not meal_id:
            return {'Message': 'Meal id is required'}, 400
        if not address:
            return {'Message': 'Address field is required'}, 400
        if not quantity:
            return {'Message': 'Quantity field is required'}, 400

        try:
            conn = db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("SELECT * FROM meals WHERE meal_id = %(mealId)s",
                        {'mealId': meal_id})

            # check if order exist
            res = cur.fetchone()
            if res is None:
                return {'Message': 'Meal does not exist'}, 400

            cur.execute("INSERT INTO orders (user_id, meal_id, quantity, address, status) VALUES (%(user_id)s, %(meal_id)s, %(quantity)s, %(address)s, %(status)s)", {
                'user_id': user_id, 'meal_id': meal_id, 'quantity': quantity, 'address': address, 'status': status})
            conn.commit()
            return {'Message': "Food item has been ordered"}, 201
        except (Exception, psycopg2.DatabaseError) as error:
            conn = db()
            cur = conn.cursor()
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

            # check if order history exist
            res = cur.fetchall()
            if not res:
                return {'Message': 'No order history'}, 404

            return {'Message': res}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            conn = db()
            cur = conn.cursor()
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
