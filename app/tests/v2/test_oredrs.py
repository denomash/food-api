# app/tests/v2/test_orders.py

import unittest
import os
import json
import jwt
import psycopg2
import psycopg2.extras

# local imports
from ... import create_app
from ...api.v2.db import test_db


class TestMenu(unittest.TestCase):
    """This class represents the orders test case"""

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
        self.user1 = {
            'email': 'deno@gmail.com',
            'password': 'aA123456'
        }

        with self.app.app_context():
            self.db = test_db()
            self.cur = self.db.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)

    def test_401_token_missing(self):
        """test 401 missing token"""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user1), content_type='application/json')
        response = self.client.get(
            '/api/v2/orders', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_404_no_history(self):
        """test 404 no order history for current user"""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user1), content_type='application/json')
        token = json.loads(res.data.decode('utf-8'))['token']
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token}
        response = self.client.get(
            '/v2/users/orders', headers=headers)
        self.assertEqual(response.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
