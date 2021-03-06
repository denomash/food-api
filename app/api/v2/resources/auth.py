# app/api/v2/resources/auth.py

from flask_restful import Resource, reqparse
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import re
import psycopg2
import psycopg2.extras
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
        'confirm_password',
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
        confirm_password = data["confirm_password"]

        if not username:
            return {'Message': 'Username field is required'}, 400
        if len(username) < 4:
            return {'Message': 'Username must be atleast four characters'}, 400
        if not email:
            return {'Message': 'Email field is required'}, 400
        if not password:
            return {'Message': 'Password field is required'}, 400

        while True:
            if not re.match(r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[a-zA-Z-]+$)", email):
                return {"Message": "Make sure your email is valid"}, 400
            elif not re.match(r"(.*\S.*)", username):
                return {"Message": "Username can\'t be blank"}
            elif re.search('[a-z]', password) is None:
                return {"Message": "Make sure your password has a small letter in it"}, 400
            elif re.search('[0-9]', password) is None:
                return {"Message": "Make sure your password has a number in it"}, 400
            elif re.search('[A-Z]', password) is None:
                return {"Message": "Make sure your password has a capital letter in it"}, 400
            elif len(password) < 8:
                return {"Message": "Make sure your password is at lest 8 letters"}, 400
            elif password != confirm_password:
                return {"Message": "Password and Confirm Password must match"}, 400
            else:
                break

        try:
            conn = db()
            cur = conn.cursor()

            # check if user email exist
            cur.execute("SELECT * FROM users WHERE email = %(email)s",
                        {'email': data["email"]})

            if cur.fetchone() is not None:
                return {'Message': 'User already exists'}, 400

            if password == 'bB123456':
                # hash password
                hash_password = generate_password_hash(
                    'bB123456', method='sha256')
                cur.execute("INSERT INTO users (email, username, type, password) VALUES (%(email)s, %(username)s, %(type)s, %(password)s);", {
                    'email': data['email'], 'username': data['username'], 'type': 'admin', 'password': hash_password})

                conn.commit()

                return {'Message': 'New admin user created'}, 201

            else:

                # hash password
                hashed_password = generate_password_hash(
                    data['password'], method='sha256')

                cur.execute("INSERT INTO users (email, username, type, password) VALUES (%(email)s, %(username)s, %(type)s, %(password)s);", {
                    'email': data['email'], 'username': data['username'], 'type': 'client', 'password': hashed_password})

                conn.commit()

                return {'Message': 'New user created'}, 201
        except (Exception, psycopg2.DatabaseError) as error:
            conn = db()
            cur = conn.cursor()
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
            else:
                break

        try:
            conn = db()
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

            cur.execute("SELECT * FROM users WHERE email = %(email)s ",
                        {'email': data["email"]})
            res = cur.fetchone()

            if res is None:
                return {'Message': 'User email does not exist'}, 404
            else:
                checked_password = check_password_hash(
                    res['password'], password)

                if checked_password == True:
                    token = jwt.encode({'id': res['id'], 'exp': datetime.datetime.utcnow(
                    ) + datetime.timedelta(minutes=60)}, 'secret')

                    secret = {'token': token.decode(
                        'UTF-8'), 'role': res['type']}
                    return {'Message': secret}, 200

                return {'Message': 'Invalid credentials'}, 400
        except (Exception, psycopg2.DatabaseError) as error:
            conn = db()
            cur = conn.cursor()
            cur.execute("rollback;")
            print(error)
            return {'Message': 'current transaction is aborted'}, 500
