from flask import make_response, jsonify, request
from .models import Order, orders_db
from flask_restplus import reqparse, Resource


class OrdersList(Resource):

    def get(self):
        """
             This method returns all orders created
        """
        if not orders_db:
            return make_response(jsonify({"message": "No parcel orders placed yet"}), 200)
        return make_response(jsonify({"orders": orders_db}), 200)

    def post(self):
        """ This method adds an order """
        parser = request.get_json()
        parcel_name = parser.get('parcel_name')
        destination = parser.get('destination')
        """ validate data sent """
        if not parcel_name or parcel_name.isspace():
            return make_response(jsonify({"message":
                                              "parcel_name field is required"}),
                                 401)
        if not destination or destination.isspace():
            return make_response(jsonify({"message":
                                              "Please add the destination of the parcel"}),
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

        order = Order(order_id,
                      parcel_name, destination, present_location, status)
        order.place_an_order()
        return make_response(jsonify({"message": "Order has been created succesfully"}), 201)


class SingleOrder(Resource):
    def get(self, order_id):
        """
            This method returns a particular order
            of the id given to it from the list of available orders
        """
        order_item = None
        for order in orders_db:
            if order['parcel_order_id'] == order_id:
                order_item = order
                return make_response(jsonify({"Order": order_item}), 200)
        return make_response(jsonify({"message": "parcel not found in our database please check the id and try again"}),
                             404)

    def put(self, order_id, action):
        """
             This method updates the status of an order.
        """
        if action == "cancel":
            for count, order in enumerate(orders_db):
                if order.get("parcel_order_id") == order_id:
                    orders_db.pop(count)
                    return make_response(jsonify({"message": "order has been deleted succesfully"}), 200)
            return make_response(jsonify({"message": "Failled to delete the order"}), 200)
        return make_response(jsonify({"message":"Incorrect action specified"}), 404)
