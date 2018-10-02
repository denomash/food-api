# app/tests/v2/test_orders.py

import unittest
import os
import json

from ... import create_app
from ...api.v2.db import test_db


class TestMenu(unittest.TestCase):
    """This class represents the bucketlist test case"""

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

    def test_404_meals_not_found(self):
        """test 404 meals not available"""
        response = self.client.get(
            '/api/v2/menu', content_type='application/json')
        res = json.loads(response.data.decode())
        self.assertEqual(res['Meals'], "No meals found")
        self.assertEqual(response.status_code, 404)

    def test_401_token_missing(self):
        """test 401 missing token"""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user1), content_type='application/json')
        response = self.client.post(
            '/api/v2/menu', content_type='application/json')
        self.assertEqual(response.status_code, 401)

    def test_401_must_be_admin(self):
        """test 401 must be admin"""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user1), content_type='application/json')
        token = json.loads(res.data.decode())['token']
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token}
        response = self.client.post(
            '/api/v2/menu', headers=headers)
        self.assertEqual(response.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
