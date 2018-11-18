import unittest
from app import create_app
from flask import current_app as app
import json, os
from app.database import Database
from .test_data import *
user = {"username":"wasibani", "email":"wasibani@me.com", "password":"12345"}
user_admin_reg = {"username":"admin", "email":"admin@me.com", "password":"admin"}
user_log = {"username":"wasibani", "password":"12345"}
user_admin = {"username":"admin", "password":"admin"}
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



    def tearDown(self):
        """method for rearing down the tables whenever a test is completed"""
        print('------Tearingdown----------------------')
        self.db.drop_table('users', 'orders')