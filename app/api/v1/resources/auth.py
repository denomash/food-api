# app/api/v1/resources/auth.py

from flask_restful import Resource, reqparse
import re

# local imports
from ..models import users


class Register(Resource):
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
        help="Number of food items is required"
    )
    parser.add_argument(
        'confirm password',
        type=str,
        required=True,
        help="Number of food items is required"
    )

    def post(self):
        """register new user"""

        data = Register.parser.parse_args()

        email = data["email"]
        password = data["password"]
        confirm_password = data["confirm password"]

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

        exist = [user for user in users if user['email'] == data['email']]

        if (len(exist) != 0):

            return {'Message': 'email alredy exist'}, 400

        user = {
            'username': data['username'],
            'email': data['email'],
            'password': data['password'],
            'confirm password': data['confirm password']
        }

        users.append(user)
        return {'User': user}, 201


class Login(Resource):
    """docstring for Login"""

    parser = reqparse.RequestParser()

    parser.add_argument(
        'email',
        type=str,
        required=True,
        help="Username required"
    )
    parser.add_argument(
        'password',
        type=str,
        required=True,
        help="Password is required"
    )

    @classmethod
    def post(self, cls):

        data = Login.parser.parse_args()
        password = data["password"]
        email = data["email"]
        validate_email = re.compile(
            r"(^[a-zA-Z0-9_.-]+@[a-zA-Z-]+\.[a-zA-Z-]+$)")

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

        if not users:
            return {'Message': 'No users found'}, 404

        for user in users:
            if email == user['email'] and password == user['password']:

                return {'Message': "User loged in successfully"}, 400

            else:
                return {'Message': 'Invalid credentials'}, 400
