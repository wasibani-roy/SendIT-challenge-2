import unittest
from app import create_app
from flask import current_app
import json
from app.parcel_order.models import Order, orders_db
from app.parcel.models import parcel_items
from .test_data import *


class BaseCase(unittest.TestCase):
    """class holds all the unittests for the app"""

    def setUp(self):
        """
            This method is run at the begining of each test
            also initialises the client where tests will be run

        """

        config_name = 'development'
        self.app = create_app(config_name)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.client = self.app.test_client

    def test_model_function(self):
        """Tests if the dummy data provided is
            an instance of the order class
        """
        self.order = Order(1, "roy parcel", "Hoima", "Kampala", "pending")
        self.assertIsInstance(self.order, Order)

    def test_app_exixts(self):
        self.assertFalse(current_app is None)

    def test_place_an_order(self):
        """
            method tests post endpoint status_code
        """
        response = self.client().post('/api/v1/orders',
                                      content_type='application/json', data=json.dumps(post_an_order))

        self.assertEqual(response.status_code, 201)

    def test_place_order_with_empty_location(self):
        """ Test for empty post validation """
        response = self.client().post("/api/v1/orders",
                                      content_type='application/json',
                                      data=json.dumps(post_with_empty_destination))
        self.assertEqual(response.status_code, 401)
        self.assertIn('Please add the destination of the parcel', str(response.data))

    def test_fetch_all_orders(self):
        "test for fetching available orders"
        response = self.client().post('/api/v1/orders',
                                      content_type='application/json', data=json.dumps(post_an_order)
                                      )
        self.assertEqual(response.status_code, 201)

        response2 = self.client().get('/api/v1/orders')
        self.assertEqual(response2.status_code, 200)

    def test_fetch_all_orders_no_orders(self):
        "test for fetching no orders"

        response = self.client().get('/api/v1/orders')
        self.assertEqual(response.status_code, 200)
        self.assertIn('No parcel orders placed yet', str(response.data))

    def test_fetch_a_single_order(self):
        """tests that get method fetches a single order"""
        response = self.client().post('/api/v1/orders',
                                      content_type='application/json', data=json.dumps(post_an_order)
                                      )
        self.assertEqual(response.status_code, 201)

        response2 = self.client().get("/api/v1/orders/1")
        self.assertEqual(response2.status_code, 200)

    def test_get_an_id_that_is_not_in_the_list(self):
        '''Test to fetch single order with wrong id'''
        response = self.client().post('/api/v1/orders',
                                      content_type='application/json', data=json.dumps(post_an_order)
                                      )
        self.assertEqual(response.status_code, 201)

        response2 = self.client().get("/api/v1/orders/2")
        self.assertEqual(response2.status_code, 404)
        self.assertIn('parcel not found in our database please check the id and try again', str(response2.data))

    def tearDown(self):
        """
        Method to tidy up lists after the test is run
        """
        orders_db[:] = []
        parcel_items[:] = []
