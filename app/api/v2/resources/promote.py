# app/api/v2/resources/promote.py

from flask_restful import Resource, reqparse
import psycopg2
import psycopg2.extras


# local imports
from ..db import db
from ..checkauth import check_auth


class Promote(Resource):
    """docstring for Promote"""

    @check_auth
    def post(current_user, self, user_id):
        if current_user["type"] != "admin":
            return {"Message": "Must be an admin"}
        parser = reqparse.RequestParser()

        parser.add_argument(
            'type',
            type=str,
            required=True,
            help="Type to promote required"

        )

        data = parser.parse_args()
        user_type = data['type']

        if not user_type:
            return {"Message": "Type to promote can\'t be blank"}
        elif user_type not in ('admin', 'client'):
            return {"Message": "Type must either be client or admin"}

        try:
            conn = db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("SELECT * FROM users WHERE id=%(user_id)s",
                        {'user_id': user_id})

            res = cur.fetchone()
            if res is None:
                return {"Message": "User with the id does not exist"}

            cur.execute("UPDATE users SET type=%s WHERE id=%s;",
                        (user_type, user_id))

            conn.commit()
            user = {}
            user['id'] = res['id']
            user['username'] = res['username']
            user['type'] = res['type']
            user['email'] = res['email']

            return {"Message": user}

        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
