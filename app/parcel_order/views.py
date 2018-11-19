from flask import make_response, jsonify, request
from .models import Order, orders_db
from app.users.models import users_data
import flask.views
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.helper import validate_data, validate_data_length


class OrdersList(flask.views.MethodView):

    def get(self):
        """
             This method returns all orders created
        """
        if not orders_db:
            return make_response(jsonify({"message": "No parcel orders placed yet"}), 200)
        return make_response(jsonify({"orders": orders_db}), 200)
    @jwt_required
    def post(self):
        """ This method adds an order """

        """Get the current user id and name"""
        current_user = get_jwt_identity()
        parser = request.get_json()
        parcel_name = parser.get('parcel_name')
        destination = parser.get('destination')
        receiver_name = parser.get('receiver')
        """ validate data sent """
        if validate_data(parcel_name):
            return make_response(jsonify({'message': 'parcel_name is required'}), 400)
        if validate_data(destination):
            return make_response(jsonify({'message': 'Please add the destination of the parcel'}), 400)
        if validate_data(receiver_name):
            return make_response(jsonify({'message': 'receiver is required'}), 400)

        if validate_data_length(destination):
            return make_response(jsonify({'message': 'Destination is to short'}), 400)

        if validate_data_length(parcel_name):
            return make_response(jsonify({'message': 'parcel_name is to short'}), 400)


        if len(orders_db) == 0:
            order_id = len(orders_db) + 1
        order_id = len(orders_db) + 1

        present_location = 'headquaters'
        status = 'pending'
        user_id = current_user['user_id']
        user_name = current_user['user_name']

        for existing_user in users_data:
            if user_id != existing_user['user_id']:
                return make_response(jsonify({"message": "Invalid user_id please go and login to continue"}), 400)

        """checking if the parcel item exists in our database"""
        for existing_order in orders_db:
            if parcel_name == existing_order["parcel_name"] and user_id == existing_order["user_id"]:
                return make_response(jsonify({"message": "parcel order has been placed before"}), 400)

        order = Order(order_id, user_id, user_name, receiver_name,
                      parcel_name, destination, present_location, status)
        order.place_an_order()
        return make_response(jsonify({"message": "Order has been created succesfully"}), 201)


class SingleOrder(flask.views.MethodView):
    def get(self, parcel_id):
        """
            This method returns a particular order
            of the id given to it from the list of available orders
        """
        order_item = None
        for order in orders_db:
            if order['parcel_order_id'] == parcel_id:
                order_item = order
                return make_response(jsonify({"Order": order_item}), 200)
        return make_response(jsonify({"message": "parcel not found in our database please check the id and try again"}),
                             404)

    def put(self, parcel_id):
        """
             This method updates the action of an order.
        """


        for count, order in enumerate(orders_db):
            if order.get("parcel_order_id") == parcel_id:
                order["status"] = "Cancelled"
                return make_response(jsonify({"message": "order has been canceled succesfully"}), 200)
        return make_response(jsonify({"message": "Failled to cancel the order"}), 400)



class UserOrder(flask.views.MethodView):
    def get(self, user_id):
        """
            This method returns a particular order
            of the user_id given to it from the list of available orders
        """
        order_item = None
        for order in orders_db:
            if order['user_id'] == user_id:
                order_item = order
                return make_response(jsonify({"Order": order_item}), 200)
        return make_response(jsonify({"message": "parcel not found in our database please check the id and try again"}),
                             404)
