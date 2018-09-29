# app/tests/v2/test_orders.py

import unittest
import os
import json
import psycopg2

from ... import create_app
from ...api.v2.fastfood import queries


class TestDB(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        app = create_app('testing')
        self.client = app.test_client()

        try:
            self.conn = psycopg2.connect(os.getenv('TEST_DB_URL'))
            self.cur = self.conn.cursor()
            self.conn.autocommit = True

            # activate connection cursor
            self.cur = self.conn.cursor()
            for query in queries:
                self.cur.execute(query)
                self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Database not connected")
            print(error)

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

    def test_201_successful_signup(self):
        """ test 201 for successfull signup"""
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_400_invalid_email(self):
        """ test 400 for invalid email"""
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.user2), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_no_lowercase_in_password(self):
        """ test 400 if password has no lowercase"""
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.user3), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_no_integer_in_password(self):
        """ test 400 if password has no integer"""
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.user4), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_no_uppercase_in_password(self):
        """ test 400 if password has no uppercase"""
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.user5), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_atleast_8_characters(self):
        """ test 400 if password atleast 8 characters"""
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.user6), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_if_confirm_password_match(self):
        """ test 400 if password confirm password match"""
        response = self.client.post(
            '/api/v1/signup', data=json.dumps(self.user7), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def tearDown(self):
        """teardown all initialized variables."""
        try:
            self.conn = psycopg2.connect(
                'dbname=test_db user=test password=test host=localhost')
            self.conn.autocommit = True

            # activate connection cursor
            self.cur = self.conn.cursor()
            self.cur.execute("DROP DATABASE test_db")
            self.conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Database not connected")
            print(error)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
