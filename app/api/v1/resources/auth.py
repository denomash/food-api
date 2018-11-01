# app/api/v1/resources/auth.py

from flask_restful import Resource, reqparse

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
        'username',
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

    def post(self):

        data = Login.parser.parse_args()
        username = data["username"]
        password = data["password"]

        if not users:
            return {'Message': 'No users found'}, 404

        for user in users:
            if username == user['username'] and password == user['password']:

                return {'User': "Login successfull"}

            elif (not username or not password):

                return {'Message': 'Fields can\'t be blank'}, 401

            elif (username != user['username'] and password != user['password']):

                return {'Message': 'Invalid credentials'}, 400

            elif (username == user['username'] and password != user['password']):

                return {'Message': 'Invalid credentials for user\'s password'}, 400

            elif (username != user['username'] and password == user['password']):

                return {'Message': 'Invalid credentials'}, 400
