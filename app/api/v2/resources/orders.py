# app/api/v1/resources/orders.py

from flask_restful import Resource, reqparse
import psycopg2
import psycopg2.extras

# local imports
from ..db import db
from ..checkauth import check_auth


class Ordersv2(Resource):
    """post an order"""

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

    parser = reqparse.RequestParser()

    parser.add_argument(
        'status',
        type=str,
        required=True,
        help="Status is required"
    )
    
    @check_auth
    def put(current_user, self, order_id):
        """create new order"""
        if current_user["type"] != "admin":
            return {"Message": "Must be an admin"}

        data = EditOrderv2.parser.parse_args()
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
