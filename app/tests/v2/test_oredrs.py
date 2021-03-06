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
        self.status = {
            "status": "status"
        }
        self.status1 = {
            "status": ""
        }
        self.status2 = {
            "status": "Complete"
        }

        with self.app.app_context():
            self.db = test_db()

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

    def test_order_related_routes(self):
        """test order related routes"""

        # login admin
        resp = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        token = json.loads(resp.data.decode('utf-8'))['token']
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token}

        # post a meal
        response = self.client.post(
            '/api/v2/menu', headers=headers, data=json.dumps(self.food))
        self.assertEqual(response.status_code, 201)

        # signup user
        response = self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(response.status_code, 201)

        # login user
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

        # test 201 user can post an order
        response = self.client.post(
            '/api/v2/users/orders', headers=headers, data=json.dumps(self.order))
        self.assertEqual(response.status_code, 201)

        # test 200 user order history found
        response = self.client.get(
            '/api/v2/users/orders', headers=headers)
        self.assertEqual(response.status_code, 200)

        # test 401 normal user can't access update status route
        response = self.client.put(
            'api/v2/orders/1', headers=headers, data=json.dumps(self.status))
        self.assertEqual(response.status_code, 401)

        # test 401 normal user can't access get order by id route
        response = self.client.get(
            'api/v2/orders/1', headers=headers)
        self.assertEqual(response.status_code, 401)

        # test 401 normal user can't access get all orders route
        response = self.client.get(
            'api/v2/orders', headers=headers)
        self.assertEqual(response.status_code, 401)

        # login admin
        resp = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        token = json.loads(resp.data.decode('utf-8'))['token']
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token}

        # test admin route 400 empty status
        response = self.client.put(
            'api/v2/orders/1', headers=headers, data=json.dumps(self.status1))
        self.assertEqual(response.status_code, 400)

        # test admin route 400 invalid status name
        response = self.client.put(
            'api/v2/orders/1', headers=headers, data=json.dumps(self.status))
        self.assertEqual(response.status_code, 400)

        # test admin update status route 400 invalid order id
        response = self.client.put(
            'api/v2/orders/12', headers=headers, data=json.dumps(self.status2))
        self.assertEqual(response.status_code, 400)

        # test 200 admin update status route
        response = self.client.put(
            'api/v2/orders/1', headers=headers, data=json.dumps(self.status2))
        self.assertEqual(response.status_code, 200)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
