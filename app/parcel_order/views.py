from flask import make_response, jsonify, request
from .models import Order, orders_db
from app.users.models import users_data
import flask.views
from app.helper import validate_data


class OrdersList(flask.views.MethodView):

    def get(self):
        """
             This method returns all orders created
        """
        if not orders_db:
            return make_response(jsonify({"message": "No parcel orders placed yet"}), 200)
        return make_response(jsonify({"orders": orders_db}), 200)

    # @login_required
    def post(self):
        """ This method adds an order """
        parser = request.get_json()
        parcel_name = parser.get('parcel_name')
        destination = parser.get('destination')
        user_name = parser.get('username')
        receiver_name = parser.get('receiver')
        user_id = parser.get('user_id')
        """ validate data sent """
        if not parcel_name or parcel_name.isspace():
            return make_response(jsonify({"message":
                                              "parcel_name field is required"}),
                                 401)
        if not destination or destination.isspace():
            return make_response(jsonify({"message":
                                              "Please add the destination of the parcel"}),
                                 401)
        if not user_name or user_name.isspace():
            return make_response(jsonify({"message":
                                              "Please add the name of person sending the parcel"}),
                                 401)
        if not receiver_name or receiver_name.isspace():
            return make_response(jsonify({"message":
                                              "Please add the recipient of the parcel"}),
                                 401)

        if len(str(destination)) < 4:
            return {'message': 'Destination is too short.'}, 400

        if len(str(parcel_name)) < 4:
            return {'message': 'parcel_name is too short.'}, 400

        """checking if the parcel item has been created and
           parcel_id exists in our database
        """

        if len(orders_db) == 0:
            order_id = len(orders_db) + 1
        order_id = len(orders_db) + 1

        present_location = 'headquaters'
        status = 'pending'

        for existing_user in users_data:
            if user_id != existing_user['user_id']:
                return make_response(jsonify({"message": "Invalid user_id please go and login to continue"}), 400)

        order = Order(order_id, user_id,user_name,receiver_name,
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
        data = request.get_json()
        action = data.get('user_action')
        if not action or action.isspace():
            return make_response(jsonify({"message":
                                              "Please add the action you want to carry out"}),
                                 401)

        if action == "cancel":
            for count, order in enumerate(orders_db):
                if order.get("parcel_order_id") == parcel_id:
                    if order["status"] == "delivered":
                        return make_response(jsonify({"message":"You are not allowed to cancel this order"}), 400)
                    order["action"] = "Cancelled"
                    return make_response(jsonify({"message": "order has been canceled succesfully"}), 200)
            return make_response(jsonify({"message": "Failled to cancel the order"}), 200)
        return make_response(jsonify({"message":"Incorrect action specified"}), 400)

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

