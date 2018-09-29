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

        self.order = {
            'item': 'pasta',
            'price': 800,
            'address': 'juja',
            'quantity': '2'
        }
        self.order2 = {
            'price': 800,
            'address': 'juja',
            'quantity': '2'
        }
        self.order3 = {
            'item': 'pasta',
            'address': 'juja',
            'quantity': '2'
        }
        self.order4 = {
            'item': 'pasta',
            'price': 800,
            'quantity': '2'
        }
        self.order5 = {
            'item': 'pasta',
            'price': 800,
            'address': 'juja'
        }


    def test_201_place_new_order(self):
        """ test 201 for posting an order successfully"""
        response = self.client.post(
            '/api/v2/orders', data=json.dumps(self.order), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_400_place_new_order_less_item(self):
        """test 400 if order has no item"""
        response = self.client.post(
            '/api/v2/orders', data=json.dumps(self.order2), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_place_new_order_less_price(self):
        """test 400 if order has no price"""
        response = self.client.post(
            '/api/v2/orders', data=json.dumps(self.order3), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_place_new_order_less_address(self):
        """test 400 if order has no address"""
        response = self.client.post(
            '/api/v2/orders', data=json.dumps(self.order4), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_place_new_order_less_quantity(self):
        """test 400 if order has no quantity"""
        response = self.client.post(
            '/api/v2/orders', data=json.dumps(self.order5), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_200_get_order_with_order_id(self):
        """test 200 if order has a valid id"""
        response = self.client.get(
            '/api/v2/orders/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_200_update_endpoint(self):
        """test 200 if order updated successfully"""
        response = self.client.put(
            '/api/v2/orders/1', data=json.dumps(self.order), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    
    def test_400_update_endpoint_status_value_empty(self):
        response = self.client.put(
            '/api/v2/orders/1', data=json.dumps(self.order9), content_type='application/json')
        res = json.loads(response.data.decode())
        self.assertEqual(res['Message'], "Status can\'t be empty")
        self.assertEqual(response.status_code, 400)

    def test_200_delete_endpoint(self):
        """test 200 if order deleted successfully"""
        response = self.client.delete(
            '/api/v2/orders/1', content_type='application/json')
        res = json.loads(response.data.decode())
        self.assertEqual(res['Message'], "Order deleted")
        self.assertEqual(response.status_code, 200)

    def tearDown(self):
        """teardown all initialized variables."""
        try:
            self.conn = psycopg2.connect(os.getenv('TEST_DB_URL'))
            self.conn.autocommit = True

            # activate connection cursor
            self.cur = self.conn.cursor()
            self.cur.execute("DROP TABLE IF EXISTS orders")
            self.conn.commit()

        except (Exception, psycopg2.DatabaseError) as error:
            print("Database not connected")
            print(error)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
