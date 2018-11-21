"""Module handles all admin related routes"""
from flask import (jsonify, make_response, request)
import flask.views
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from app.helper import is_not_valid_order
from .models import Order


class AdminOrderLocation(flask.views.MethodView):
    """This class handles the update location route"""

    @jwt_required
    def put(self, parcel_id):
        """This method updates the location of a parcel order"""
        current_user = get_jwt_identity()
        if current_user['username'] == "admin":
            parser = request.get_json()
            present_location = parser.get('location')
            order = Order(user_id=None, parcel_name=None, order_id=parcel_id, \
                          receiver_name=None, status=None,
                          deliver_status=None \
                          , destination=None, present_location=present_location.lower())
            if is_not_valid_order(present_location.strip()):
                return make_response(jsonify({'message': 'present location is incorrect'}), 400)

            update_present_location = order.update_present_location()
            if update_present_location:
                return make_response(jsonify({'message': \
                                                  'present location updated succesfully'}), 200)
            return make_response(jsonify({'message': \
                                              'Failed to update present location'}), 400)
        return make_response(jsonify({"message": \
                                          "You are not authorised to access this resource"}), 401)


class AdminOrderStatus(flask.views.MethodView):
    """This handles the user update delivery status route"""

    @jwt_required
    def put(self, parcel_id):
        """Method to update deliver status of a specific route"""
        current_user = get_jwt_identity()
        if current_user['username'] == "admin":
            parser = request.get_json()
            deliver_status = parser.get('delivery_status')
            order = Order(user_id=None, parcel_name=None, order_id=parcel_id, \
                          receiver_name=None, status=None,
                          deliver_status=deliver_status.lower() \
                          , destination=None, present_location=None)
            if is_not_valid_order(deliver_status.strip()):
                return make_response(jsonify({'message': \
                                                  'Delivery status is incorrect'}), 400)

            update_status = order.update_delivery_status()
            if update_status:
                return make_response(jsonify({'message': \
                                                  'Delivery status updated succesfully'}), 200)
            return make_response(jsonify({'message': \
                                              'Failed to update delivery status'}), 400)
        return make_response(jsonify({"message": \
                                          "You are not authorised to access this resource"}), 401)
