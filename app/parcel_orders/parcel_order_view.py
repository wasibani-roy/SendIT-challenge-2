from flask import jsonify, make_response
from .models import Order
from flask import request
import flask.views
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.helper import *

class ParcelOrder(flask.views.MethodView):
    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        if current_user['username'] == "admin":
            orders = Order.order_history()
            if not orders:
                return make_response(jsonify({"message": "No orders placed so far"}), 200)
            return make_response(jsonify({"Parcel orders": orders}), 200)
        else:
            return make_response(jsonify({"message": "You are not authorised to access this resource"}), 401)

    @jwt_required
    def post(self):
        current_user = get_jwt_identity()
        """ Receiving request data from users"""
        parser = request.get_json()
        parcel_name = parser.get('parcel_name')
        destination = parser.get('destination')
        receiver_name = parser.get('receiver')
        """Validate the data before use"""
        if validate_not_order_detail_string(parcel_name):
            return make_response(jsonify({"Message": "parcel_name must be a string"}), 400)
        if validate_not_order_detail_string(destination):
            return make_response(jsonify({"Message": "destination must be a string"}), 400)
        if validate_not_order_detail_string(receiver_name):
            return make_response(jsonify({"Message": "receiver name must be a string"}), 400)
        if validate_no_data(parcel_name):
            return make_response(jsonify({"Message": "parcel_name is required"}), 400)
        if validate_no_data(destination):
            return make_response(jsonify({"Message": "destination is required"}), 400)
        if validate_no_data(receiver_name):
            return make_response(jsonify({"Message": "receiver name is required"}), 400)

        status = "pending"
        present_location = "Headquaters"
        deliver_status = "pending"
        user_id = current_user["user_id"]

        """creating an insatnce of an order class"""
        order = Order(order_id=None, user_id=user_id, parcel_name=parcel_name.lower(), receiver_name=receiver_name.lower(), \
                      destination=destination.lower(), status=status.lower(), present_location=present_location.lower(),
                      deliver_status=deliver_status.lower())
        select_order = order.fetch_parcel_name()
        if select_order:
            return make_response(jsonify({'message': 'Order has already been placed'}), 403)
        create_order = order.insert_order_data()
        if create_order:
            return make_response(jsonify({'messege': "you have succesfully placed order"}), 201)
        return make_response(jsonify({"message": "Order not placed succesfully"}), 400)
