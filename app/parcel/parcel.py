"""This module handles the parcels route"""
from flask import (jsonify, make_response, request)
import flask.views
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flasgger import swag_from
from app.helper import (is_not_valid_order, validate_not_keys)
from .models import Order


class ParcelOrder(flask.views.MethodView):
    """Class handling post and get routes"""
    @jwt_required
    @swag_from('../docs/get_orders.yml', methods=['GET'])
    def get(self):
        """Method to get all orders"""
        current_user = get_jwt_identity()
        if Order.fetch_role(current_user["user_id"]) == "admin":
            orders = Order.order_history()
            if not orders:
                return make_response(jsonify({"message": "No orders placed so far"}), 200)
            return make_response(jsonify({"Parcel orders": orders}), 200)

        return make_response(jsonify({"message": \
                                          "You are not authorised to access this resource"}), 401)

    @jwt_required
    @swag_from('../docs/post_parcel.yml', methods=['POST'])
    def post(self):
        """Method handling post a parcel order by logged in user"""
        current_user = get_jwt_identity()
        # Receiving request data from users
        parser = request.get_json()
        if validate_not_keys(parser, 4):
            return make_response(jsonify({"message": "Some fields are missing!"}), 400)
        parcel_name = parser.get('parcel_name')
        destination = parser.get('destination')
        receiver_name = parser.get('receiver')
        price = parser.get('price')
        # Validate the data before use
        if is_not_valid_order(parcel_name.strip()):
            return make_response(jsonify({"message": "parcel_name is incorrect"}), 400)
        if is_not_valid_order(destination.strip()):
            return make_response(jsonify({"Message": "destination is in correct"}), 400)
        if is_not_valid_order(receiver_name.strip()):
            return make_response(jsonify({"Message": "receiver name is incorrect"}), 400)

        status = "pending"
        present_location = "Headquaters"
        deliver_status = "pending"
        user_id = current_user["user_id"]

        # creating an insatnce of an order class
        order = Order(order_id=None, user_id=user_id, parcel_name=parcel_name.lower(),
                      receiver_name=receiver_name.lower(),
                      destination=destination.lower(), status=status.lower(),
                      present_location=present_location.lower(),
                      deliver_status=deliver_status.lower(), price=price)
        select_order = order.fetch_parcel_name()
        if select_order:
            return make_response(jsonify({'message': 'Order has already been placed'}), 403)
        create_order = order.insert_order_data()
        if create_order:
            return make_response(jsonify({'messege': "you have succesfully placed order"}), 201)
        return make_response(jsonify({"message": "Order not placed succesfully"}), 400)
