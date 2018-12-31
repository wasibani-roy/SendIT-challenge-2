"""Module handles all admin related routes"""
from flask import (jsonify, make_response, request)
import flask.views
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flasgger import swag_from
from app.helper import (is_not_valid_order, validate_not_keys, is_not_valid_destination)
from .models import Order


class AdminOrderLocation(flask.views.MethodView):
    """This class handles the update location route"""

    @jwt_required
    @swag_from('../docs/put_location.yml', methods=['PUT'])
    def put(self, parcel_id):
        """This method updates the location of a parcel order"""
        current_user = get_jwt_identity()
        if Order.fetch_role(current_user["user_id"]) == "admin":
            parser = request.get_json()
            if validate_not_keys(parser, 1):
                return make_response(jsonify({"message": "Some fields are missing!"}), 400)
            present_location = parser.get('location')
            order = Order(user_id=None, parcel_name=None, order_id=parcel_id, \
                          receiver_name=None, status=None,
                          deliver_status=None \
                          , destination=None, present_location=present_location.lower(), price=None)
            if is_not_valid_destination(present_location.strip()):
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
    @swag_from('../docs/put_status.yml', methods=['PUT'])
    def put(self, parcel_id):
        """Method to update deliver status of a specific route"""
        current_user = get_jwt_identity()
        if Order.fetch_role(current_user["user_id"]) == "admin":
            parser = request.get_json()
            if len(parser.keys()) != 1:
                return make_response(jsonify({"message": "Some fields are missing!"}), 400)
            deliver_status = parser.get('delivery_status')
            order = Order(user_id=None, parcel_name=None, order_id=parcel_id, \
                          receiver_name=None, status=None,
                          deliver_status=deliver_status.lower() \
                          , destination=None, present_location=None, price=None)
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


class AdminSearchOrder(flask.views.MethodView):
    """This class handles the get and put routes of users orders"""
    @jwt_required
    def post(self):
        """Method handling the Admin search"""
        current_user = get_jwt_identity()
        if Order.fetch_role(current_user["user_id"]) == "admin":
            parser = request.get_json()
            if len(parser.keys()) != 1:
                return make_response(jsonify({"message": "Some fields are missing!"}), 400)
            search_item = parser.get('search_item')
            order = Order(user_id=None, parcel_name=search_item, order_id=None, \
                          receiver_name=None, status=None,
                          deliver_status=None \
                          , destination=None, present_location=None, price=None)
            if is_not_valid_order(search_item.strip()):
                return make_response(jsonify({'message': 'please enter search item'}), 400)

            search_order = order.search_admin_order()
            if search_order:
                return make_response(jsonify(search_order), 200)
            return make_response(jsonify({'message': 'Error in search'}), 400)
        return make_response(jsonify({"message": \
                                          "You are not authorised to access this resource"}), 401)