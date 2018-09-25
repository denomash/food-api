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
            'status': 'pending'
        }
        self.order2 = {
            'item': 'pasta',
            'price': 800,
            'address': 'juja',
            'quantity': '2'
        }
        self.order3 = {
            'status': 'completed'
        }
        self.order4 = {
            'status': 'complete'
        }
        self.order5 = {
            'price': 800,
            'address': 'juja',
            'quantity': '2'
        }
        self.order6 = {
            'item': 'pasta',
            'address': 'juja',
            'quantity': '2'
        }
        self.order7 = {
            'item': 'pasta',
            'price': 800,
            'quantity': '2'
        }
        self.order8 = {
            'item': 'pasta',
            'price': 800,
            'address': 'juja'
        }
        self.order9 = {
            'status': ''
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

    def test_201_place_new_order(self):
        """ test 201 for posting an order successfully"""
        response = self.client.post(
            '/api/v1/orders', data=json.dumps(self.order2), content_type='application/json')
        self.assertEqual(response.status_code, 201)

    def test_400_place_new_order_less_item(self):
        """test 400 if order has no item"""
        response = self.client.post(
            '/api/v1/orders', data=json.dumps(self.order5), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_place_new_order_less_price(self):
        """test 400 if order has no price"""
        response = self.client.post(
            '/api/v1/orders', data=json.dumps(self.order6), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_place_new_order_less_address(self):
        """test 400 if order has no address"""
        response = self.client.post(
            '/api/v1/orders', data=json.dumps(self.order7), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_400_place_new_order_less_quantity(self):
        """test 400 if order has no quantity"""
        response = self.client.post(
            '/api/v1/orders', data=json.dumps(self.order8), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_200_get_order_with_order_id(self):
        """test 200 if order has a valid id"""
        order_data.append(self.order)
        response = self.client.get(
            '/api/v1/orders/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_200_update_endpoint(self):
        """test 200 if order updated successfully"""
        order_data.append(self.order)
        response = self.client.put(
            '/api/v1/orders/1', data=json.dumps(self.order3), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_400_update_endpoint_wrong_status_value(self):
        """test 400 if status has wrong status value"""
        order_data.append(self.order)
        response = self.client.put(
            '/api/v1/orders/1', data=json.dumps(self.order4), content_type='application/json')        
        res = json.loads(response.data.decode())
        self.assertEqual(res['Message'], "Status must be either pending or completed")
        self.assertEqual(response.status_code, 400)

    def test_400_update_endpoint_status_value_empty(self):
        """test 400 if status is empty"""
        order_data.append(self.order)
        response = self.client.put(
            '/api/v1/orders/1', data=json.dumps(self.order9), content_type='application/json')
        res = json.loads(response.data.decode())
        self.assertEqual(res['Message'], "Status can\'t be empty")
        self.assertEqual(response.status_code, 400)

    def test_200_delete_endpoint(self):
        """test 200 if order deleted successfully"""
        order_data.append(self.order)
        response = self.client.delete(
            '/api/v1/orders/1', content_type='application/json')
        res = json.loads(response.data.decode())
        self.assertEqual(res['Message'], "Order deleted")
        self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
