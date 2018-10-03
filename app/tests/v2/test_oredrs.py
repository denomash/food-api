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
        self.admin = {
            'email': 'admin@gmail.com',
            'password': 'aA123456'
        }
        self.food = {
            "item": "pizza",
            "price": 500,
            "description": "fried"
        }
        self.order = {
            "mealId": "1",
            "quantity": 5,
            "address": "K-Road"
        }
        self.order1 = {
            "mealId": "",
            "quantity": 5,
            "address": "K-Road"
        }
        self.order2 = {
            "mealId": "1",
            "quantity": "",
            "address": "K-Road"
        }
        self.order3 = {
            "mealId": "1",
            "quantity": 5,
            "address": ""
        }
        self.order4 = {
            "mealId": "12",
            "quantity": 5,
            "address": "K-Road"
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
        self.assertEqual(response.status_code, 404)

    def test_user_orders(self):
        """test user order routes"""
        resp = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        token = json.loads(resp.data.decode('utf-8'))['token']
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token}
        response = self.client.post(
            '/api/v2/menu', headers=headers, data=json.dumps(self.food))
        self.assertEqual(response.status_code, 201)
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user1), content_type='application/json')
        self.assertEqual(res.status_code, 200)

        token = json.loads(res.data.decode('utf-8'))['token']
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token}

        # test 400 empty meal id
        response = self.client.post(
            '/api/v2/users/orders', headers=headers, data=json.dumps(self.order1))
        self.assertEqual(response.status_code, 400)

        # test 400 empty quantity field
        response = self.client.post(
            '/api/v2/users/orders', headers=headers, data=json.dumps(self.order2))
        self.assertEqual(response.status_code, 400)

        # test 400 empty address field
        response = self.client.post(
            '/api/v2/users/orders', headers=headers, data=json.dumps(self.order3))
        self.assertEqual(response.status_code, 400)

        # test 400 invalid meal id while making order
        response = self.client.post(
            '/api/v2/users/orders', headers=headers, data=json.dumps(self.order4))
        self.assertEqual(response.status_code, 400)

        # test 404 no user order history found
        response = self.client.get(
            '/api/v2/users/orders', headers=headers)
        self.assertEqual(response.status_code, 404)

        # test user can post a meal
        response = self.client.post(
            '/api/v2/users/orders', headers=headers, data=json.dumps(self.order))
        self.assertEqual(response.status_code, 201)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
