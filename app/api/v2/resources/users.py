# app/api/v2/resources/users.py

from flask_restful import Resource, reqparse
import psycopg2
import psycopg2.extras


# local imports
from ..db import db
from ..checkauth import check_auth


class Users(Resource):
    """docstring for Promote"""

    @check_auth
    def get(current_user, self):
        if current_user["type"] != "admin":
            return {"Message": "Must be an admin"}, 401

        try:
            conn = db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute("SELECT * FROM users")
            res = cur.fetchall()

            if res is None:
                return {"Message": "No users found"}, 404

            return {"Users": res}, 200

        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
