# app/api/v1/resources/orders.py

from flask_restful import Resource, reqparse
import psycopg2

# local imports
from ..db import db
from ..models import get_by_id, is_empty


class Get_ordersv2(Resource):
    """docstring for Order"""

    def get(self):
        """get all orders"""
        try:
            conn = db()
            cur = conn.cursor()
            cur.execute("SELECT * from orders")
            orders = cur.fetchall()

            return {"Message": orders}
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
