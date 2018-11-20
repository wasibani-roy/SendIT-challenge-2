from flask import jsonify, make_response
from app.helper import *
from .models import Order
from flask import request
import flask.views
from flask_jwt_extended import jwt_required, get_jwt_identity


class AdminOrderLocation(flask.views.MethodView):

    @jwt_required
    def put(self, parcel_id):
        current_user = get_jwt_identity()
        if current_user['username'] == "admin":
            parser = request.get_json()
            present_location = parser.get('present_location')
            order = Order(user_id=None, parcel_name=None, order_id=parcel_id, receiver_name=None, status=None,
                          deliver_status=None \
                          , destination=None, present_location=present_location.lower())
            if validate_not_order_detail_string(present_location):
                return make_response(jsonify({'Message': 'present location must be a string'}), 400)
            if validate_no_data(present_location):
                return make_response(jsonify({'Message': 'Please enter the present location'}), 400)

            update_present_location = order.update_present_location()
            if update_present_location:
                return make_response(jsonify({'Message': 'present location updated succesfully'}), 200)
            return make_response(jsonify({'Message': 'Failed to update present location'}), 400)
        return make_response(jsonify({"Message": "You are not authorised to access this resource"}), 401)


class AdminOrderStatus(flask.views.MethodView):
    @jwt_required
    def put(self, parcel_id):
        current_user = get_jwt_identity()
        if current_user['username'] == "admin":
            parser = request.get_json()
            deliver_status = parser.get('delivery_status')
            order = Order(user_id=None, parcel_name=None, order_id=parcel_id, receiver_name=None, status=None,
                          deliver_status=deliver_status.lower() \
                          , destination=None, present_location=None)
            if validate_not_order_detail_string(deliver_status):
                return make_response(jsonify({'Message': 'Delivery status must be a string'}), 400)
            if validate_no_data(deliver_status):
                return make_response(jsonify({'Message': 'Please enter the delivery status'}), 400)

            update_status = order.update_delivery_status()
            if update_status:
                return make_response(jsonify({'Message': 'Delivery status updated succesfully'}), 200)
            return make_response(jsonify({'Message': 'Failed to update delivery status'}), 400)
        return make_response(jsonify({"Message": "You are not authorised to access this resource"}), 401)
