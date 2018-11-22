"""This is the test class for parcel end points"""
import json
from tests.test_base_case import BaseCase


class SenditParcelTestCase(BaseCase):
    """This class tests the parcel end points"""

    def test_post_parcel_order(self):
        """method for testing posting an order endpoint"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_login"]), \
            content_type='application/json')
        response = self.client.post('api/v2/parcels', \
                                    data=json.dumps(self.parcel["valid_parcel"]), \
                                    content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 201)
        self.assertIn('you have succesfully placed order', str(response.data))

    def test_post_parcel_order_invalid_data(self):
        """method for testing post order endpoint invalid data"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_login"]), \
            content_type='application/json')
        response = self.client.post('api/v2/parcels', \
                                    data=json.dumps(self.parcel["invalid_parcel_name"]),
                                    content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 400)

    def test_post_parcel_order_multiple_times(self):
        """method for testing post order endpoint with invalid data"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/',\
            data=json.dumps(self.user_login["valid_login"]), content_type='application/json')
        self.client.post('api/v2/parcels', data=json.dumps(self.parcel["valid_parcel"]),
                         content_type='application/json',
                         headers={'Authorization': self.get_token()})
        response = self.client.post('api/v2/parcels', \
                                    data=json.dumps(self.parcel["valid_parcel"]), \
                                    content_type='application/json',
                                    headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 403)
        self.assertIn('Order has already been placed', str(response.data))

    def test_get_parcel_orders_admin(self):
        """method for testing Admin get all orders"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/',\
            data=json.dumps(self.user_login["valid_login"]), content_type='application/json')
        self.client.post('api/v2/parcels', \
                         data=json.dumps(self.parcel["valid_parcel"]), \
                         content_type='application/json',
                         headers={'Authorization': self.get_token()})
        self.create_admin_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_admin_login"]), \
            content_type='application/json')
        response = self.client.get('/api/v2/parcels', content_type='application/json',
                                   headers={'Authorization': self.get_admin_token()})
        self.assertEqual(response.status_code, 200)

    def test_get_parcel_orders_admin_no_authorised(self):
        """method for testing Admin get all orders"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/',\
            data=json.dumps(self.user_login["valid_login"]), content_type='application/json')
        self.client.post('api/v2/parcels', data=json.dumps(self.parcel["valid_parcel"]),
                         content_type='application/json',
                         headers={'Authorization': self.get_token()})
        self.create_admin_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_login"]), \
            content_type='application/json')
        response = self.client.get('/api/v2/parcels', content_type='application/json',
                                   headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 401)

    def test_get_parcel_orders_admin_no_orders(self):
        """method for testing Admin get no orders"""
        self.create_admin_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_admin_login"]), \
            content_type='application/json')
        response = self.client.get('/api/v2/parcels', \
                                   content_type='application/json',
                                   headers={'Authorization': self.get_admin_token()})
        self.assertEqual(response.status_code, 200)

    def test_set_present_location(self):
        """method for testing Admin change present location"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_login"]), content_type='application/json')
        self.client.post('api/v2/parcels', data=json.dumps(self.parcel["valid_parcel"]), \
                         content_type='application/json',
                         headers={'Authorization': self.get_token()})
        self.create_admin_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_admin_login"]), \
            content_type='application/json')
        response = self.client.put('api/v2/parcels/1/presentLocation', \
                                   data=json.dumps(self.parcel_update["location"]),
                                   content_type='application/json',
                                   headers={'Authorization': self.get_admin_token()})
        self.assertEqual(response.status_code, 200)

    def test_set_present_location_no_location(self):
        """method for testing Admin change present location no location"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_login"]), content_type='application/json')
        self.client.post('api/v2/parcels', \
                         data=json.dumps(self.parcel["valid_parcel"]), \
                         content_type='application/json',
                         headers={'Authorization': self.get_token()})
        self.create_admin_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_admin_login"]), \
            content_type='application/json')
        response = self.client.put('api/v2/parcels/1/presentLocation', \
                                   data=json.dumps(self.parcel_update["invalid_location"]), \
                                   content_type='application/json',
                                   headers={'Authorization': self.get_admin_token()})
        self.assertEqual(response.status_code, 400)

    def test_set_present_location_not_authorised(self):
        """method for testing Admin change present location no location"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_login"]), \
            content_type='application/json')
        self.client.post('api/v2/parcels', \
                         data=json.dumps(self.parcel["valid_parcel"]), \
                         content_type='application/json',
                         headers={'Authorization': self.get_token()})
        self.create_admin_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_admin_login"]), \
            content_type='application/json')
        response = self.client.put('api/v2/parcels/1/presentLocation', \
                                   content_type='application/json',
                                   headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 401)

    def test_set_delivery_status(self):
        """method for testing Admin change delivery status"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_login"]), content_type='application/json')
        self.client.post('api/v2/parcels', \
                         data=json.dumps(self.parcel["valid_parcel"]), \
                         content_type='application/json',
                         headers={'Authorization': self.get_token()})
        self.create_admin_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_admin_login"]), \
            content_type='application/json')
        response = self.client.put('api/v2/parcels/1/status', \
                                   data=json.dumps(self.parcel_update["delivery_status"]),
                                   content_type='application/json',
                                   headers={'Authorization': self.get_admin_token()})
        self.assertEqual(response.status_code, 200)

    def test_get_user_parcel_orders(self):
        """method for testing get users orders endpoint"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_login"]), \
            content_type='application/json')
        self.client.post('api/v2/parcels', \
                         data=json.dumps(self.parcel["valid_parcel"]), \
                         content_type='application/json',
                         headers={'Authorization': self.get_token()})
        response = self.client.get('/api/v2/parcels/user',
                                   headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 200)

    def test_get_user_parcel_no_orders(self):
        """method for testing no user orders made"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_login"]), \
            content_type='application/json')
        response = self.client.get('/api/v2/parcels/user',
                                   headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 404)

    def test_update_destination(self):
        """method for testing user change destination"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_login"]), \
            content_type='application/json')
        self.client.post('api/v2/parcels', \
                         data=json.dumps(self.parcel["valid_parcel"]), \
                         content_type='application/json',
                         headers={'Authorization': self.get_token()})
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_admin_login"]), \
            content_type='application/json')
        response = self.client.put('api/v2/parcels/1/destination',
                                   data=json.dumps(self.parcel_update["destination"]),
                                   content_type='application/json',
                                   headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 200)

    def test_get_user_parcel_specific_order(self):
        """method for testing get a particular users order"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_login"]), content_type='application/json')
        self.client.post('api/v2/parcels', \
                         data=json.dumps(self.parcel["valid_parcel"]), \
                         content_type='application/json',
                         headers={'Authorization': self.get_token()})
        response = self.client.get('/api/v2/parcels/user/1',
                                   headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 200)

    def test_get_user_parcel_specific_order_not(self):
        """method for testing get no order"""
        self.create_valid_user()
        self.client.post(
            '/api/v2/auth/login/', \
            data=json.dumps(self.user_login["valid_login"]), content_type='application/json')
        response = self.client.get('/api/v2/parcels/user/1',
                                   headers={'Authorization': self.get_token()})
        self.assertEqual(response.status_code, 404)
