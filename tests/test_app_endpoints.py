import unittest, flask
from app import create_app
from flask import current_app, session
import json
from app.parcel_order.models import Order, orders_db
from app.parcel.models import parcel_items
from app.users.models import users_data
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

    # def test_model_function(self):
    #     """Tests if the dummy data provided is
    #         an instance of the order class
    #     """
    #     self.order = Order(1, "roy parcel", "Hoima", "Kampala", "pending")
    #     self.assertIsInstance(self.order, Order)

    def test_app_exixts(self):
        self.assertFalse(current_app is None)

    def test_place_an_order(self):
        """
            method tests post endpoint status_code
        """
        self.client().post('/api/v1/signup',
                           content_type='application/json', data=json.dumps(user_register_data)
                           )
        self.client().post('/api/v1/login',
                           content_type='application/json', data=json.dumps(user_login_data)
                           )
        response = self.client().post('/api/v1/parcels/',
                                      content_type='application/json', data=json.dumps(post_an_order))

        self.assertEqual(response.status_code, 201)

    def test_place_an_order_multiple_times(self):
        """
            method tests post an order with same data
        """
        self.client().post('/api/v1/signup',
                           content_type='application/json', data=json.dumps(user_register_data)
                           )
        self.client().post('/api/v1/login',
                           content_type='application/json', data=json.dumps(user_login_data)
                           )
        self.client().post('/api/v1/parcels/',
                                      content_type='application/json', data=json.dumps(post_an_order))
        response = self.client().post('/api/v1/parcels/',
                                      content_type='application/json', data=json.dumps(post_an_order))

        self.assertEqual(response.status_code, 400)

    def test_place_order_with_empty_location(self):
        """ Test for empty post validation """
        response = self.client().post("/api/v1/parcels",
                                      content_type='application/json',
                                      data=json.dumps(post_with_empty_destination))
        self.assertEqual(response.status_code, 401)
        self.assertIn('Please add the destination of the parcel', str(response.data))

    def test_fetch_all_orders(self):
        "test for fetching available orders"
        response = self.client().post('/api/v1/signup',
                                      content_type='application/json', data=json.dumps(user_register_data)
                                      )
        response2 = self.client().post('/api/v1/login',
                                       content_type='application/json', data=json.dumps(user_login_data)
                                       )
        response3 = self.client().post('/api/v1/parcels',
                                       content_type='application/json', data=json.dumps(post_an_order)
                                       )
        self.assertEqual(response.status_code, 201)

        response4 = self.client().get('/api/v1/parcels')
        self.assertEqual(response4.status_code, 200)

    def test_fetch_all_orders_no_orders(self):
        "test for fetching no orders"

        response = self.client().get('/api/v1/parcels')
        self.assertEqual(response.status_code, 200)
        self.assertIn('No parcel orders placed yet', str(response.data))

    def test_fetch_a_single_order(self):
        """tests that get method fetches a single order"""
        response = self.client().post('/api/v1/signup',
                                      content_type='application/json', data=json.dumps(user_register_data)
                                      )
        response2 = self.client().post('/api/v1/login',
                                       content_type='application/json', data=json.dumps(user_login_data)
                                       )
        response3 = self.client().post('/api/v1/parcels',
                                       content_type='application/json', data=json.dumps(post_an_order)
                                       )
        self.assertEqual(response3.status_code, 201)

        response4 = self.client().get("/api/v1/parcels/1")
        self.assertEqual(response4.status_code, 200)

    def test_get_an_id_that_is_not_in_the_list(self):
        '''Test to fetch single order with wrong id'''
        self.client().post('/api/v1/signup',
                           content_type='application/json', data=json.dumps(user_register_data)
                           )
        self.client().post('/api/v1/login',
                           content_type='application/json', data=json.dumps(user_login_data)
                           )
        self.client().post('/api/v1/parcels',
                           content_type='application/json', data=json.dumps(post_an_order)
                           )

        response2 = self.client().get("/api/v1/parcels/2")
        self.assertEqual(response2.status_code, 404)
        self.assertIn('parcel not found in our database please check the id and try again', str(response2.data))

    def test_change_parcel_action_to_cancelled(self):
        '''Test to cancel an order'''
        self.client().post('/api/v1/signup',
                           content_type='application/json', data=json.dumps(user_register_data)
                           )
        self.client().post('/api/v1/login',
                           content_type='application/json', data=json.dumps(user_login_data)
                           )
        self.client().post('/api/v1/parcels',
                           content_type='application/json', data=json.dumps(post_an_order)
                           )
        # self.assertEqual(response3.status_code, 201)

        response2 = self.client().put("/api/v1/parcels/1/cancel", content_type='application/json', \
                                      data=json.dumps(user_action_data))
        self.assertEqual(response2.status_code, 200)

    def test_change_parcel_action_to_cancelled_invalid_action(self):
        '''Test to cancel an order invalid action status'''
        self.client().post('/api/v1/signup',
                           content_type='application/json', data=json.dumps(user_register_data)
                           )
        self.client().post('/api/v1/login',
                           content_type='application/json', data=json.dumps(user_login_data)
                           )
        self.client().post('/api/v1/parcels',
                           content_type='application/json', data=json.dumps(post_an_order)
                           )
        # self.assertEqual(response3.status_code, 201)

        response = self.client().put("/api/v1/parcels/1/cancel", content_type='application/json', \
                                     data=json.dumps(user_action_data_invalid_action))
        self.assertEqual(response.status_code, 400)
        self.assertIn('Incorrect action specified', str(response.data))

    def test_change_parcel_action_to_cancelled_no_action(self):
        '''Test to cancel an order invalid action status'''
        self.client().post('/api/v1/signup',
                           content_type='application/json', data=json.dumps(user_register_data)
                           )
        self.client().post('/api/v1/login',
                           content_type='application/json', data=json.dumps(user_login_data)
                           )
        self.client().post('/api/v1/parcels',
                           content_type='application/json', data=json.dumps(post_an_order)
                           )
        # self.assertEqual(response3.status_code, 201)

        response = self.client().put("/api/v1/parcels/1/cancel", content_type='application/json', \
                                     data=json.dumps(user_action_data_no_action))
        self.assertEqual(response.status_code, 401)
        self.assertIn('Please add the action you want to carry out', str(response.data))

    def test_user_registration(self):
        """
            method tests post endpoint status_code
        """
        response = self.client().post('/api/v1/signup',
                                      content_type='application/json', data=json.dumps(user_register_data)
                                      )

        self.assertEqual(response.status_code, 201)

    def test_user_registration_multiple_registration(self):
        """
            method tests registering with same details
        """
        self.client().post('/api/v1/signup',
                                      content_type='application/json', data=json.dumps(user_register_data)
                                      )
        response = self.client().post('/api/v1/signup',
                                      content_type='application/json', data=json.dumps(user_register_data)
                                      )

        self.assertEqual(response.status_code, 400)
        self.assertIn('username already exists', str(response.data))

    def test_user_registration_invalid_data_username(self):
        """
            method tests post endpoint status_code
        """
        response = self.client().post('/api/v1/signup',
                                      content_type='application/json',
                                      data=json.dumps(user_register_data_invalid_username)
                                      )

        self.assertEqual(response.status_code, 401)

    def test_user_registration_invalid_data_email(self):
        """
            method tests post endpoint status_code
        """
        response = self.client().post('/api/v1/signup',
                                      content_type='application/json', data=json.dumps(user_register_data_invalid_email)
                                      )

        self.assertEqual(response.status_code, 401)

    def test_user_registration_invalid_length_username(self):
        """
            method tests length of password validation
        """
        response = self.client().post('/api/v1/signup',
                                      content_type='application/json',
                                      data=json.dumps(user_register_data_invalid_username_len)
                                      )

        self.assertEqual(response.status_code, 400)
        self.assertIn('username is to short', str(response.data))

    def test_user_registration_invalid_data_password(self):
        """
            method tests post endpoint status_code
        """
        response = self.client().post('/api/v1/signup',
                                      content_type='application/json',
                                      data=json.dumps(user_register_data_invalid_password)
                                      )

        self.assertEqual(response.status_code, 401)

    def test_user_registration_invalid_length_password(self):
        """
            method tests length of password validation
        """
        response = self.client().post('/api/v1/signup',
                                      content_type='application/json',
                                      data=json.dumps(user_register_data_invalid_password_len)
                                      )

        self.assertEqual(response.status_code, 400)
        self.assertIn('password is too short', str(response.data))

    def test_user_login(self):
        """
            method tests post endpoint status_code
        """
        self.client().post('/api/v1/signup',
                           content_type='application/json', data=json.dumps(user_register_data)
                           )
        response = self.client().post('/api/v1/login',
                                      content_type='application/json', data=json.dumps(user_login_data)
                                      )

        self.assertEqual(response.status_code, 200)

    def test_user_login_invalid_username(self):
        """
            method tests login with invalid username
        """
        self.client().post('/api/v1/signup',
                           content_type='application/json', data=json.dumps(user_register_data)
                           )
        response = self.client().post('/api/v1/login',
                                      content_type='application/json', data=json.dumps(user_login_data_invalid_name)
                                      )

        self.assertIn('incorrect username and password', str(response.data))

    def test_user_login_invalid_username_data(self):
        """
            method tests login with no username
        """
        self.client().post('/api/v1/signup',
                           content_type='application/json', data=json.dumps(user_register_data)
                           )
        response = self.client().post('/api/v1/login',
                                      content_type='application/json', data=json.dumps(user_login_data_invalid_username)
                                      )

        self.assertIn('user_name field is required', str(response.data))

    def test_user_login_invalid_password_data(self):
        """
            method tests login with no password
        """
        self.client().post('/api/v1/signup',
                           content_type='application/json', data=json.dumps(user_register_data)
                           )
        response = self.client().post('/api/v1/login',
                                      content_type='application/json', data=json.dumps(user_login_data_invalid_password)
                                      )

        self.assertIn('Please add you,re password', str(response.data))

    def test_fetch_a_users_orders(self):
        """tests that get method fetches a single order"""
        self.client().post('/api/v1/signup',
                           content_type='application/json', data=json.dumps(user_register_data)
                           )
        self.client().post('/api/v1/login',
                           content_type='application/json', data=json.dumps(user_login_data)
                           )
        self.client().post('/api/v1/parcels',
                           content_type='application/json', data=json.dumps(post_an_order)
                           )

        response = self.client().get("/api/v1/users/1/parcels")
        self.assertEqual(response.status_code, 200)

    def test_fetch_a_users_orders_invalid_id(self):
        """tests that get method fetches a single order"""
        self.client().post('/api/v1/signup',
                           content_type='application/json', data=json.dumps(user_register_data)
                           )
        self.client().post('/api/v1/login',
                           content_type='application/json', data=json.dumps(user_login_data)
                           )
        self.client().post('/api/v1/parcels',
                           content_type='application/json', data=json.dumps(post_an_order)
                           )

        response = self.client().get("/api/v1/users/2/parcels")
        self.assertEqual(response.status_code, 404)

    def test_get_user(self):
        """
            method tests getting all registered users
        """
        self.client().post('/api/v1/signup',
                           content_type='application/json', data=json.dumps(user_register_data)
                           )
        self.client().post('/api/v1/login',
                           content_type='application/json', data=json.dumps(user_login_data)
                           )
        response = self.client().get('/api/v1/signup/')

        self.assertEqual(response.status_code, 200)

    def test_no_user(self):
        """
            method tests getting no registered users
        """
        response = self.client().get('/api/v1/signup/')

        self.assertEqual(response.status_code, 200)
        self.assertIn('No Registered users', str(response.data))

    def tearDown(self):
        """
        Method to tidy up lists after the test is run
        """
        orders_db[:] = []
        parcel_items[:] = []
        users_data[:] = []
