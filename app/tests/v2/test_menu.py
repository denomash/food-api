# app/tests/v2/test_orders.py

import unittest
import os
import json
import psycopg2

from ... import create_app
from ...api.v2.db import test_db


class TestDB(unittest.TestCase):
    """This class represents the bucketlist test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app('testing')
        self.client = self.app.test_client()

        with self.app.app_context():
            self.db = test_db()

    def test_404_meals_not_found(self):
        """test 404 meals not available"""
        response = self.client.get(
            '/api/v2/menu', content_type='application/json')
        self.assertEqual(response.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
