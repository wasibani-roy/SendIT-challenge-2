"""This is the base test class for setting up my tests"""
import unittest
import json
from app import create_app
from app.database import Database

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

        self.user = {
            "valid_user": {"username": "wasibani", "email": "roy@me.com", "password": "12345", "role": "user"},
            "invalid_username": {"username": "", "email": "roy@me.com", "password": "12345", "role":"user"},
            "invalid_email": {"username": "wasibani", "email": "", "password": "12345", "role":"user"},
            "invalid_password": {"username": "wasibani", "email": "roy@me.com", "password": "", "role": "user"},
            "valid_admin": {"username": "admin", "email": "admin@me.com", "password": "admin", "role": "admin"},
        }
        self.user_login = {
            "valid_login": {"username": "wasibani", "password": "12345"},
            "invalid_username": {"username": "", "password": "12345"},
            "invalid_password": {"username": "wasibani", "password": ""},
            "invalid_credentials": {"username": "wasibani", "password": "wasiba"},
            "valid_admin_login": {"username": "admin", "password": "admin"}
        }
        self.parcel = {
            "valid_parcel": {"parcel_name": "chairs", "destination": "jinja", "receiver": "danny", "price":12000},
            "invalid_parcel_name": {"parcel_name": "", "destination": "jinja", "receiver": "danny", "price": 12000},
            "ivalid_destination": {"parcel_name": "chairs", "destination": "", "receiver": "danny", "price": 12000},
            "invalid_receiver": {"parcel_name": "chairs", "destination": "jinja", "receiver": "", "price": 12000},
        }
        self.parcel_update = {
            "destination": {"destination": "wandegeya"},
            "location": {"location": "Jinja"},
            "invalid_location": {"location": ""},
            "delivery_status": {"delivery_status": "delivered"}
        }

    def create_valid_user(self):
        """ Registers a user to be used for tests"""
        response = self.client.post('/api/v2/auth/signup/',
                                    data=json.dumps(self.user["valid_user"]),
                                    content_type='application/json')
        return response

    def create_admin_user(self):
        """ Registers a user to be used for tests"""
        response = self.client.post('/api/v2/auth/signup/',
                                    data=json.dumps(self.user["valid_admin"]),
                                    content_type='application/json')
        return response

    def get_token(self):
        ''' Generates a toke to be used for tests'''
        response = self.client.post('/api/v2/auth/login',
                                    data=json.dumps(self.user_login["valid_login"]),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        return 'Bearer ' + data['access token']

    def get_admin_token(self):
        ''' Generates a toke to be used for tests'''
        response = self.client.post('/api/v2/auth/login',
                                    data=json.dumps(self.user_login["valid_admin_login"]),
                                    content_type='application/json')
        data = json.loads(response.data.decode())
        return 'Bearer ' + data['access token']

    def tearDown(self):
        """method for rearing down the tables whenever a test is completed"""
        self.db.drop_table('users', 'orders')
