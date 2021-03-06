# app/tests/v2/test_orders.py

import unittest
import os
import json

from ... import create_app
from ...api.v2.db import test_db


class TestLogin(unittest.TestCase):
    """This class represents the login test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.user = {
            'email': 'deno@gmail.com',
            'password': ''
        }
        self.user2 = {
            'email': '',
            'password': 'aA123456'
        }
        self.user3 = {
            'email': 'denogmail.com',
            'password': 'aA123456'
        }
        self.user4 = {
            'email': 'deno@gmail.com',
            'password': '2A123456'
        }
        self.user5 = {
            'email': 'deno@gmail.com',
            'password': 'aAgfydfgh'
        }
        self.user6 = {
            'email': 'denogmail.com',
            'password': 'ak123456'
        }
        self.user7 = {
            'email': 'deno@gmail.com',
            'password': 'aA12345'
        }
        self.user8 = {
            'username': 'deno',
            'email': 'deno@gmail.com',
            'password': 'aA123456',
            'confirm password': 'aA123456'
        }
        self.user9 = {
            'email': 'man@gmail.com',
            'password': 'aA123456'
        }
        self.user10 = {
            'email': 'deno@gmail.com',
            'password': 'bB123456'
        }
        self.user11 = {
            'email': 'deno@gmail.com',
            'password': 'aA123456'
        }

        with self.app.app_context():
            self.db = test_db()

    def test_400_empty_password(self):
        """ test 400 for empty password"""
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_empty_email(self):
        """ test 400 for empty email"""
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user2), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_invalid_email(self):
        """ test 400 for invalid email"""
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user3), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_no_lowercase_in_password(self):
        """ test 400 if password has no lowercase"""
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user4), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_no_integer_in_password(self):
        """ test 400 if password has no integer"""
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user5), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_no_uppercase_in_password(self):
        """ test 400 if password has no uppercase"""
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user6), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_atleast_8_characters(self):
        """ test 400 if password atleast 8 characters"""
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user7), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_404_if_user_does_not_exist(self):
        """test 404 if user does not exists"""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user8), content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user9), content_type='application/json')
        self.assertEqual(res.status_code, 404)

    def test_400_login_invalid_credentials(self):
        """test 400 invalid credentials"""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user8), content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user10), content_type='application/json')
        self.assertEqual(res.status_code, 400)

    def test_200_user_logged_in_successfully(self):
        """test 200 successfull login"""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user8), content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user11), content_type='application/json')
        self.assertEqual(res.status_code, 200)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
