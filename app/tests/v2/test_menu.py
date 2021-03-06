# app/tests/v2/test_orders.py

import unittest
import json

# local imports
from ... import create_app
from ...api.v2.db import test_db


class TestMenu(unittest.TestCase):
    """This class represents the menu test case"""

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
        self.food1 = {
            "item": "",
            "price": 500,
            "description": "fried"
        }
        self.food2 = {
            "item": "pizza",
            "price": "",
            "description": "fried"
        }
        self.food3 = {
            "item": "pizza",
            "price": 500,
            "description": ""
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
        resp = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user1), content_type='application/json')
        token = json.loads(resp.data.decode('utf-8'))['token']
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
        response = self.client.post(
            '/api/v2/menu', data=json.dumps(self.food), headers=headers)
        self.assertEqual(response.status_code, 401)

    def test_400_no_item(self):
        """test 400 when admin posts an empty item field"""
        resp = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        token = json.loads(resp.data.decode('utf-8'))['token']
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
        response = self.client.post(
            '/api/v2/menu', data=json.dumps(self.food1), headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_400_no_price(self):
        """test 400 when admin posts an empty price field"""
        resp = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        token = json.loads(resp.data.decode('utf-8'))['token']
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
        response = self.client.post(
            '/api/v2/menu', data=json.dumps(self.food2), headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_400_no_description(self):
        """test 400 when admin posts an empty description field"""
        resp = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        token = json.loads(resp.data.decode('utf-8'))['token']
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
        response = self.client.post(
            '/api/v2/menu', data=json.dumps(self.food3), headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_400_meal_already_exist(self):
        """test 400 meal exists if admin try to add a meal twice"""
        resp = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        token = json.loads(resp.data.decode('utf-8'))['token']
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
        self.client.post(
            '/api/v2/menu', data=json.dumps(self.food), headers=headers)
        response = self.client.post(
            '/api/v2/menu', data=json.dumps(self.food), headers=headers)
        self.assertEqual(response.status_code, 400)

    def test_201_meal_created_successfully(self):
        """test 201 meal added successfully by admin"""
        resp = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        token = json.loads(resp.data.decode('utf-8'))['token']
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token
        }
        response = self.client.post(
            '/api/v2/menu', data=json.dumps(self.food), headers=headers)
        self.assertEqual(response.status_code, 201)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
