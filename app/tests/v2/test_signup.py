# app/tests/v2/test_orders.py

import unittest
import json

from ... import create_app
from ...api.v2.db import test_db


class TestSignup(unittest.TestCase):
    """This class represents the Signup test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.user = {
            'username': 'deno',
            'email': 'deno@gmail.com',
            'password': 'aA123456',
            'confirm password': 'aA123456'
        }
        self.user2 = {
            'username': 'deno',
            'email': 'denogmail.com',
            'password': 'aA123456',
            'confirm password': 'aA123456'
        }
        self.user3 = {
            'username': 'deno',
            'email': 'deno@gmail.com',
            'password': '2A123456',
            'confirm password': 'aA123456'
        }
        self.user4 = {
            'username': 'deno',
            'email': 'deno@gmail.com',
            'password': 'aAhdjhhdh',
            'confirm password': 'aA123456'
        }
        self.user5 = {
            'username': 'deno',
            'email': 'deno@gmail.com',
            'password': 'af123456',
            'confirm password': 'aA123456'
        }
        self.user6 = {
            'username': 'deno',
            'email': 'deno@gmail.com',
            'password': 'aA12345',
            'confirm password': 'aA123456'
        }
        self.user7 = {
            'username': 'deno',
            'email': 'deno@gmail.com',
            'password': 'aA1234567',
            'confirm password': 'aA123456'
        }

        with self.app.app_context():
            self.db = test_db()

    def test_400_invalid_email(self):
        """ test 400 for invalid email"""
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user2), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_no_lowercase_in_password(self):
        """ test 400 if password has no lowercase"""
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user3), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_no_integer_in_password(self):
        """ test 400 if password has no integer"""
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user4), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_no_uppercase_in_password(self):
        """ test 400 if password has no uppercase"""
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user5), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_atleast_8_characters(self):
        """ test 400 if password atleast 8 characters"""
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user6), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_if_confirm_password_match(self):
        """ test 400 if password confirm password match"""
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user7), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_201_register_successfull(self):
        """test 201 for loggin successfull"""
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_400_if_user_already_exist(self):
        """test 400 if user exists"""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(res.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
