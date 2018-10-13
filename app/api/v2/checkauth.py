
from flask import request
import jwt
from functools import wraps
import psycopg2
import psycopg2.extras


from .db import db

def check_auth(f):

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return {'Message': 'You don\'t have a token!'}, 401

        try:
            data = jwt.decode(token, 'secret')
            conn = db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("SELECT * FROM users WHERE id = %(id)s ",
                        {'id': data["id"]})
            current_user = cur.fetchone()

        except:
            return {'Message': 'Invalid token!'}, 401

        return f(current_user, *args, **kwargs)

    return decorated