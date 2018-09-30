# app/api/v2/resources/auth.py

from flask_restful import Resource, reqparse
import jwt
import re
import psycopg2
import datetime

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

        email = data["email"]
        password = data["password"]
        confirm_password = data["confirm password"]

        if not email:
            return {'Message': 'Email field is required'}, 400
        if not password:
            return {'Message': 'Password field is required'}, 400

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
                return {'Message': 'User already exists'}, 400

            cur.execute("INSERT INTO users (email, username, type, password) VALUES (%(email)s, %(username)s, %(type)s, %(password)s);", {
                'email': data['email'], 'username': data['username'], 'type': 'client', 'password': data['password']})

            conn.commit()

            return {'Message': 'New user created'}, 201
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500


class LoginV2(Resource):
    """docstring for Login"""

    parser = reqparse.RequestParser()

    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="Email required"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Password is required"
    )

    def post(self):

        data = LoginV2.parser.parse_args()
        password = data["password"]
        email = data["email"]
        validate_email = re.compile(
            r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[a-zA-Z-]+$)")

        if not email:
            return {'Message': 'Email field is required'}, 400
        if not password:
            return {'Message': 'Password field is required'}, 400

        while True:
            if not (re.match(validate_email, email)):
                return {"Message": "Make sure your email is valid"}, 400
            elif re.search('[a-z]', password) is None:
                return {"Message": "Make sure your password has a small letter in it"}, 400
            elif re.search('[0-9]', password) is None:
                return {"Message": "Make sure your password has a number in it"}, 400
            elif re.search('[A-Z]', password) is None:
                return {"Message": "Make sure your password has a capital letter in it"}, 400
            elif len(password) < 8:
                return {"Message": "Make sure your password is at lest 8 letters"}, 400
            else:
                break

        try:
            conn = db()
            cur = conn.cursor()

            cur.execute("SELECT * FROM users WHERE email = %(email)s and password = %(password)s",
                        {'email': data["email"], 'password': data['password']})
            # check if user email exist

            user = cur.fetchone()

            if user is None:
                return {'Message': 'Invalid credentials'}, 400
            else:
                token = jwt.encode({'id': user[0], 'exp': datetime.datetime.utcnow(
                ) + datetime.timedelta(minutes=30)}, 'secret')
                return {'token': token.decode('UTF-8')}
                return {'Message': 'User logged in successfully'}, 200
        except (Exception, psycopg2.DatabaseError) as error:
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
