# app/tests/v2/test_orders.py

import unittest
import json

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
        self.admin = {
            'email': 'admin@gmail.com',
            'password': 'aA123456'
        }
        self.type = {
            'type': 'admin'
        }

        with self.app.app_context():
            self.db = test_db()

    
    def test_200_user_promoted_successfully(self):
        """test 200 successfull login"""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        response = self.client.post(
            '/api/v2/promote/1', data=json.dumps(self.type), content_type='application/json')
        self.assertEqual(response.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
