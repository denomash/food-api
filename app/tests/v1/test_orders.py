# app/api/tests/v1/test_orders.py

import unittest
import json

from ... import create_app
from ...api.v1.models import order_data


class Order_tests(unittest.TestCase):
    """docstring for Order_tests"""

    def setUp(self):
        app = create_app('testing')
        self.client = app.test_client()
        self.order = {
            'id': 1,
            'item': 'pizza',
            'price': 900,
            'quantity': '4',
            'delivered': False
        }
        self.order2 = {
            'item': 'pasta',
            'price': 800,
            'address': 'juja',
            'quantity': '2'
        }

    def test_404_get_all_orders(self):
        """ test 404 if order found"""
        response = self.client.get(
            '/api/v1/orders', content_type='application/json')
        res = json.loads(response.data.decode())
        if not order_data:
            self.assertEqual(res['Message'], "No orders found")
            self.assertEqual(response.status_code, 404)

    def test_200_get_all_orders(self):
        """ test 200 if order found"""
        response = self.client.get(
            '/api/v1/orders', content_type='application/json')
        if order_data:
            self.assertIn("Order", response)
            self.assertEqual(response.status_code, 200)

    def test_place_new_order(self):
        response = self.client.post(
            '/api/v1/orders', data=json.dumps(self.order2), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_get_order_with_order_id(self):
        order_data.append(self.order)
        response = self.client.get(
            '/api/v1/orders/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
