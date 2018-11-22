"""This is the test class for login and registration end points"""
import json
from tests.test_base_case import BaseCase


class SenditAuthTestCase(BaseCase):
    """This class tests the registration and login end points"""

    def test_user_registration(self):
        """This function tests user registration"""
        response = self.create_valid_user()
        self.assertEqual(response.status_code, 201)
        self.assertIn('you have succesfully signed up', str(response.data))

    def test_user_registration_invalid_username(self):
        """This function test registration with invalid username"""
        response = self.client.post('/api/v2/auth/signup/',
                                    data=json.dumps(self.user["invalid_username"]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Please supply a username\
                 of 4 or more characters', str(response.data))

    def test_user_registration_invalid_password(self):
        """This function tests registration with invalid password"""
        response = self.client.post('/api/v2/auth/signup/',
                                    data=json.dumps(self.user["invalid_password"]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Password is incorrect', str(response.data))

    def test_user_registration_invalid_email(self):
        """This function tests registration with invalid email"""
        response = self.client.post('/api/v2/auth/signup/',
                                    data=json.dumps(self.user["invalid_email"]),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('email is incorrect', str(response.data))

    def test_user_resgistration_register_multiple_times(self):
        """This function tests registration multiple times"""
        self.create_valid_user()
        response = self.create_valid_user()
        self.assertEqual(response.status_code, 403)
        self.assertIn('Username already exists', str(response.data))

    def test_user_login(self):
        """method for testing user_login endpoint"""
        self.create_valid_user()
        response = self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_login"]), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        print(response.data)
        data = json.loads(response.data.decode())
        self.assertTrue(data['access token'])

    def test_user_login_invalid_password(self):
        """method for testing user_login endpoint"""
        self.create_valid_user()
        response = self.client.post(
            '/api/v2/auth/login/', data=json.dumps(self.user_login["invalid_credentials"]),
            content_type='application/json')
        self.assertEqual(response.status_code, 401)
        self.assertIn('Invalid credentials', str(response.data))

    def test_user_login_invalid_username(self):
        """method for testing user_login endpoint"""
        self.create_valid_user()
        response = self.client.post(
            '/api/v2/auth/login/', data=json.dumps(self.user_login["invalid_username"]),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('Username is incorrect', str(response.data))
