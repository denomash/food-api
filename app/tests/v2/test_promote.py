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
        self.type1 = {
            'type': ''
        }
        self.type2 = {
            'type': 'admi'
        }

        with self.app.app_context():
            self.db = test_db()

    def test_promote_endpoint(self):
        """test 200 successfull login"""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        self.assertEqual(res.status_code, 200)
        token = json.loads(res.data.decode('utf-8'))['token']
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token}

        # test 400 type empty
        response = self.client.post(
            '/api/v2/promote/1', headers=headers, data=json.dumps(self.type1))
        self.assertEqual(response.status_code, 400)

        # test 400 wrong type
        response = self.client.post(
            '/api/v2/promote/1', headers=headers, data=json.dumps(self.type2))
        self.assertEqual(response.status_code, 400)

        # test 200 user promoted successfully
        response = self.client.post(
            '/api/v2/promote/1', headers=headers, data=json.dumps(self.type))
        self.assertEqual(response.status_code, 200)

        # test 404 user does not exist
        response = self.client.post(
            '/api/v2/promote/11', headers=headers, data=json.dumps(self.type))
        self.assertEqual(response.status_code, 404)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
