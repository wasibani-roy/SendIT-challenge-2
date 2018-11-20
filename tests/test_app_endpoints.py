import unittest
from app import create_app
import json
from app.database import Database
from .test_data import *

class BaseCase(unittest.TestCase):
    """class holds all the unittests for the endpoints"""

    def setUp(self):
        """
            This method is run at the begining of each test
            also initialises the client where tests will be run

        """
        config_name = 'testing'
        self.app = create_app(config_name)
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.db = Database()
        self.db.create_tables()
        self.client = self.app.test_client()

    def create_valid_user(self):
        """ Registers a user to be used for tests"""
        response = self.client.post('/api/v2/auth/signup/',
                                    data=json.dumps(user_register_data),
                                    content_type='application/json')
        return response

    def create_admin_user(self):
        """ Registers a user to be used for tests"""
        response = self.client.post('/api/v2/auth/signup/',
                                    data=json.dumps(admin_register_data),
                                    content_type='application/json')
        return response

    def get_token(self):
        ''' Generates a toke to be used for tests'''
        response = self.client.post('/api/v2/auth/login',
                                    data=json.dumps(user_login_data),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        return 'Bearer ' + data['access token']

    def get_admin_token(self):
        ''' Generates a toke to be used for tests'''
        response = self.client.post('/api/v2/auth/login',
                                    data=json.dumps(admin_login_data),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        return 'Bearer ' + data['access token']


    def test_user_resgistration(self):
        response = self.create_valid_user()
        self.assertEqual(response.status_code, 201)
        self.assertIn('you have succesfully signed up', str(response.data))

    def test_user_resgistration_invalid_username(self):
        response = self.client.post('/api/v2/auth/signup/',
                                    data=json.dumps(user_register_data_invalid_username),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username is required', str(response.data))

    def test_user_resgistration_invalid_password(self):
        response = self.client.post('/api/v2/auth/signup/',
                                    data=json.dumps(user_register_data_invalid_password),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Password is required', str(response.data))

    def test_user_resgistration_invalid_email(self):
        response = self.client.post('/api/v2/auth/signup/',
                                    data=json.dumps(user_register_data_invalid_email),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email is required', str(response.data))

    def test_user_resgistration_invalid_email_structure(self):
        response = self.client.post('/api/v2/auth/signup/',
                                    data=json.dumps(user_register_data_invalid_email_structure),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('please input a valid email', str(response.data))

    def test_user_resgistration_invalid_email_structure1(self):
        response = self.client.post('/api/v2/auth/signup/',
                                    data=json.dumps(user_register_data_invalid_email_structure2),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('please input valid email', str(response.data))

    def test_user_resgistration_register_multiple_times(self):
        self.create_valid_user()
        response = self.create_valid_user()
        self.assertEqual(response.status_code, 403)
        self.assertIn('Username already exists', str(response.data))

    def test_user_login(self):
        """method for testing user_login endpoint"""
        self.create_valid_user()
        response = self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print(response.data)
        data = json.loads(response.data.decode())
        self.assertTrue(data['access token'])

    def test_user_login_invalid_password(self):
        """method for testing user_login endpoint"""
        self.create_valid_user()
        response = self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data_invalid_password), content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', str(response.data))

    def test_user_login_invalid_username(self):
        """method for testing user_login endpoint"""
        self.create_valid_user()
        response = self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data_invalid_name), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username must contain only characters', str(response.data))

    def test_post_parcel_order(self):
        """method for testing posting an order endpoint"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data_invalid_name), content_type='application/json')
        response = self.client.post('api/v2/parcels', data=json.dumps(post_an_order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 201)
        self.assertIn('you have succesfully placed order', str(response.data))

    def test_post_parcel_order_invalid_data(self):
        """method for testing post order endpoint invalid data"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data_invalid_name), content_type='application/json')
        response = self.client.post('api/v2/parcels', data=json.dumps(post_an_order_invalid_data_post), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 400)
        # self.assertIn('you have succesfully placed order', str(response.data))

    def test_post_parcel_order_multiple_times(self):
        """method for testing post order endpoint invalid data"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        self.client.post('api/v2/parcels', data=json.dumps(post_an_order),
                         content_type='application/json',
                         headers={'Authorization': self.get_token()})
        response = self.client.post('api/v2/parcels', data=json.dumps(post_an_order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 403)
        self.assertIn('Order has already been placed', str(response.data))

    def test_get_parcel_orders_admin(self):
        """method for testing Admin get all orders"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        self.client.post('api/v2/parcels', data=json.dumps(post_an_order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.create_admin_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(admin_login_data), content_type='application/json')
        response = self.client.get('/api/v2/parcels', content_type='application/json',
                                    headers={'Authorization': self.get_admin_token()})
        self.assertEqual(response.status_code, 200)

    def test_get_parcel_orders_admin_no_authorised(self):
        """method for testing Admin get all orders"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        self.client.post('api/v2/parcels', data=json.dumps(post_an_order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.create_admin_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        response = self.client.get('/api/v2/parcels', content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 401)

    def test_get_parcel_orders_admin_no_orders(self):
        """method for testing Admin get no orders"""
        self.create_admin_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(admin_login_data), content_type='application/json')
        response = self.client.get('/api/v2/parcels', content_type='application/json',
                                    headers={'Authorization': self.get_admin_token()})
        self.assertEqual(response.status_code, 200)

    def test_set_present_location(self):
        """method for testing Admin change present location"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        self.client.post('api/v2/parcels', data=json.dumps(post_an_order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.create_admin_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        response = self.client.put('api/v2/parcels/1/presentLocation', data=json.dumps(admin_change_location), content_type='application/json',
                                    headers={'Authorization': self.get_admin_token()})
        self.assertEqual(response.status_code, 200)

    def test_set_present_location_no_location(self):
        """method for testing Admin change present location no location"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        self.client.post('api/v2/parcels', data=json.dumps(post_an_order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.create_admin_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        response = self.client.put('api/v2/parcels/1/presentLocation',  content_type='application/json',
                                    headers={'Authorization': self.get_admin_token()})
        self.assertEqual(response.status_code, 400)

    def test_set_present_location_not_authorised(self):
        """method for testing Admin change present location no location"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        self.client.post('api/v2/parcels', data=json.dumps(post_an_order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.create_admin_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        response = self.client.put('api/v2/parcels/1/presentLocation',  content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 401)

    def test_set_delivery_status(self):
        """method for testing Admin change delivery status"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        self.client.post('api/v2/parcels', data=json.dumps(post_an_order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.create_admin_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        response = self.client.put('api/v2/parcels/1/status', data=json.dumps(admin_delivery_status), content_type='application/json',
                                    headers={'Authorization': self.get_admin_token()})
        self.assertEqual(response.status_code, 200)

    def test_get_user_parcel_orders(self):
        """method for testing get users orders endpoint"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        self.client.post('api/v2/parcels', data=json.dumps(post_an_order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        response = self.client.get('/api/v2/parcels/user',
                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 200)

    def test_get_user_parcel_no_orders(self):
        """method for testing no user orders made"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        response = self.client.get('/api/v2/parcels/user',
                                   headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 404)

    def test_update_destination(self):
        """method for testing user change destination"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        self.client.post('api/v2/parcels', data=json.dumps(post_an_order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(admin_login_data), content_type='application/json')
        response = self.client.put('api/v2/parcels/1/destination',
                                   data=json.dumps(update_destination),
                                   content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 200)

    def test_get_user_parcel_specific_order(self):
        """method for testing get a particular users order"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        self.client.post('api/v2/parcels', data=json.dumps(post_an_order), content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        response = self.client.get('/api/v2/parcels/user/1',
                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 200)

    def test_get_user_parcel_specific_order_not(self):
        """method for testing get no order"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', data=json.dumps(user_login_data), content_type='application/json')
        response = self.client.get('/api/v2/parcels/user/1',
                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 404)





    def tearDown(self):
        """method for rearing down the tables whenever a test is completed"""
        self.db.drop_table('users', 'orders')