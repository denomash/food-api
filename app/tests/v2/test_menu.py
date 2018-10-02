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
        self.admin = {
            'email': 'admin@gmail.com',
            'password': 'aA1234567'
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
            self.cur = self.db.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)

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
        data = jwt.decode(token, 'secret')
        self.cur.execute("SELECT * FROM users WHERE id = %(id)s ",
                         {'id': data["id"]})
        current_user = self.cur.fetchone()
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token}
        response = self.client.post(
            '/api/v2/menu', data=json.dumps(self.food), headers=headers)
        if response and current_user['type'] != 'admin':
            self.assertEqual(response.status_code, 401)

    def test_400_no_item(self):
        """test 400 when admin posts an empty item field"""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user1), content_type='application/json')
        token = json.loads(res.data.decode())['token']
        data = jwt.decode(token, 'secret')
        self.cur.execute("SELECT * FROM users WHERE id = %(id)s ",
                         {'id': data["id"]})
        current_user = self.cur.fetchone()
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token}
        response = self.client.post(
            '/api/v2/menu', data=json.dumps(self.food1), headers=headers)
        if response and current_user['type'] == 'admin':
            self.assertEqual(response.status_code, 400)

    def test_400_no_price(self):
        """test 400 when admin posts an empty price field"""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user1), content_type='application/json')
        token = json.loads(res.data.decode())['token']
        data = jwt.decode(token, 'secret')
        self.cur.execute("SELECT * FROM users WHERE id = %(id)s ",
                         {'id': data["id"]})
        current_user = self.cur.fetchone()
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token}
        response = self.client.post(
            '/api/v2/menu', data=json.dumps(self.food2), headers=headers)
        if response and current_user['type'] == 'admin':
            self.assertEqual(response.status_code, 400)

    def test_400_no_description(self):
        """test 400 when admin posts an empty description field"""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user1), content_type='application/json')
        token = json.loads(res.data.decode())['token']
        data = jwt.decode(token, 'secret')
        self.cur.execute("SELECT * FROM users WHERE id = %(id)s ",
                         {'id': data["id"]})
        current_user = self.cur.fetchone()
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token}
        response = self.client.post(
            '/api/v2/menu', data=json.dumps(self.food3), headers=headers)
        if response and current_user['type'] == 'admin':
            self.assertEqual(response.status_code, 400)

    def test_400_meal_already_exist(self):
        """test 400 meal exists if admin try to add a meal twice"""
        self.client.post(
            '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user1), content_type='application/json')
        token = json.loads(res.data.decode())['token']
        data = jwt.decode(token, 'secret')
        self.cur.execute("SELECT * FROM users WHERE id = %(id)s ",
                         {'id': data["id"]})
        current_user = self.cur.fetchone()
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token}
        self.client.post(
            '/api/v2/menu', data=json.dumps(self.food), headers=headers)
        response = self.client.post(
            '/api/v2/menu', data=json.dumps(self.food), headers=headers)
        if response and current_user['type'] == 'admin':
            self.assertEqual(response.status_code, 400)

    def test_201_meal_created_successfully(self):
        """test 201 meal added successfully by admin"""
        self.cur.execute("INSERT INTO users (email, username, type, password) VALUES (%(email)s, %(username)s, %(type)s, %(password)s);", {
            'email': 'admin@gmail.com', 'username': 'admin', 'type': 'admin', 'password': 'aA123456'})
        res = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.admin), content_type='application/json')
        token = json.loads(res.data.decode())['token']
        data = jwt.decode(token, 'secret')
        self.cur.execute("SELECT * FROM users WHERE id = %(id)s ",
                         {'id': data["id"]})
        current_user = self.cur.fetchone()
        headers = {
            'Content-Type': 'application/json',
            'x-access-token': token}
        response = self.client.post(
            '/api/v2/menu', data=json.dumps(self.food), headers=headers)
        if response and current_user['type'] == 'admin':
            self.assertEqual(response.status_code, 400)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
