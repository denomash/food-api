# app/api/v2/resources/auth.py

from flask_restful import Resource, reqparse
import re
import psycopg2

# local imports
from ..db import db


class Registerv2(Resource):
    """docstring for Register"""
    parser = reqparse.RequestParser()

    parser.add_argument(
        'username',
        type=str,
        required=True,
        help="Username required"
    )
    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="Email is required"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Password is required"
    )
    parser.add_argument(
        'confirm password',
        type=str,
        required=True,
        help="Confirm password is required"
    )

    def post(self):
        """register new user"""

        data = Registerv2.parser.parse_args()

        username = data["username"]
        email = data["email"]
        password = data["password"]
        confirm_password = data["confirm password"]

        if not username:
            return {'Message': 'Username field is required'}
        if not email:
            return {'Message': 'Email field is required'}
        if not password:
            return {'Message': 'Password field is required'}
        if not confirm_password:
            return {'Message': 'Confirm password field is required'}

        while True:
            if not re.match(r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[a-zA-Z-]+$)", email):
                return {"Message": "Make sure your email is valid"}, 400
            elif re.search('[a-z]', password) is None:
                return {"Message": "Make sure your password has a small letter in it"}, 400
            elif re.search('[0-9]', password) is None:
                return {"Message": "Make sure your password has a number in it"}, 400
            elif re.search('[A-Z]', password) is None:
                return {"Message": "Make sure your password has a capital letter in it"}, 400
            elif len(password) < 8:
                return {"Message": "Make sure your password is at lest 8 letters"}, 400
            elif password != confirm_password:
                return {"Message": "password and confirm_password must be the same"}, 400
            else:
                break

        try:
            conn = db()
            cur = conn.cursor()

            cur.execute("SELECT * FROM users WHERE email = %(email)s",
                        {'email': data["email"]})
            # check if user email exist

            if cur.fetchone() is not None:
                return {'Message': 'User already exists'}

            cur.execute("INSERT INTO users (email, username, password, confirm_password) VALUES (%(email)s, %(username)s, %(password)s, %(confirm_password)s);", {
                'email': data['email'], 'username': data['username'], 'password': data['password'], 'confirm_password': data['confirm password']})

            conn.commit()

            return {'Message': 'New user created'}
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}
