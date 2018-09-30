import unittest
import json

from ... import create_app
from ...api.v2.db import test_db, init_db


class TestDb(unittest.TestCase):

    def setUp(self):
        from app import create_app
        self.app = create_app('testing')
        self.client = self.app.test_client()
        self.user = {
            'email': 'deno@gmail.com',
            'password': 'aA12345'
        }

        with self.app.app_context():
            self.db = test_db()

    def test_base(self):
        res = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_200_login(self):
        """ test 400 for empty password"""
        response = self.client.post(
            '/api/v2/auth/login', data=json.dumps(self.user), content_type='application/json')
        self.assertEqual(response.status_code, 200)

if __name__ == "__main__":
    unittest.main()
