"""Module handles the user order routes"""
from flask import (jsonify, make_response, request)
import flask.views
from flask_jwt_extended import (jwt_required, get_jwt_identity)
from flasgger import swag_from
from app.helper import is_not_valid_order
from .models import Order


class UserSpecificOrder(flask.views.MethodView):
    """This class handles the get and put routes of users orders"""

    @jwt_required
    @swag_from('../docs/user_get_orders.yml', methods=['GET'])
    def get(self):
        """Method handling the get a specific users parcel orders"""
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        new_order = Order(user_id=user_id, parcel_name=None, order_id=None, \
                          receiver_name=None, status=None,
                          deliver_status=None \
                          , destination=None, present_location=None, price=None)
        order = new_order.user_orders()
        if not order:
            return make_response(jsonify({'message': "you have no orders at this time"}), 404)
        return make_response(jsonify(order), 200)

    @jwt_required
    @swag_from('../docs/put_destination.yml', methods=['PUT'])
    def put(self, parcel_id):
        """Method handling the update of destination"""
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        parser = request.get_json()
        if len(parser.keys()) != 1:
            return make_response(jsonify({"message": "Some fields are missing!"}), 400)
        destination = parser.get('destination')
        order = Order(user_id=user_id, parcel_name=None, order_id=parcel_id, \
                      receiver_name=None, status=None,
                      deliver_status=None \
                      , destination=destination.lower(), present_location=None, price=None)
        if is_not_valid_order(destination.strip()):
            return make_response(jsonify({'message': 'destination incorrect'}), 400)
        if order.check_delivery_status():
            return make_response(jsonify({"message": "You can not change the destination of a delivered product"}), \
                                 400)

        update_destination = order.update_destination()
        if update_destination:
            return make_response(jsonify({'message': 'destination updated succesfully'}), 200)
        return make_response(jsonify({'message': 'Failed to update destination'}), 400)


class UserSpecificOrderById(flask.views.MethodView):
    """This class handles get route for specific user order"""

    @jwt_required
    @swag_from('../docs/user_get_specific_order.yml', methods=['GET'])
    def get(self, parcel_id):
        """Method handling the get a specific users parcel order by id"""
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        new_order = Order(user_id=user_id, parcel_name=None, order_id=parcel_id, \
                          receiver_name=None, status=None,
                          deliver_status=None \
                          , destination=None, present_location=None, price=None)
        order = new_order.single_order()
        if not order:
            return make_response(jsonify({'message': \
                                              "This parcel order doesn't\
                                               exist please check id and try again"}),
                                 404)
        return make_response(jsonify({'orders': order}), 200)

    @jwt_required
    def put(self, parcel_id):
        """Method handling the canceling of an order"""
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        new_status = "cancelled"
        order = Order(user_id=user_id, parcel_name=None, order_id=parcel_id, \
                      receiver_name=None, status=new_status,
                      deliver_status=None \
                      , destination=None, present_location=None, price=None)
        if order.check_delivery_status():
            return make_response(jsonify({"message": "You can not cancel a delivered product"}), \
                                 400)

        update_status = order.update_user_status()
        if update_status:
            return make_response(jsonify({'message': 'You have successfully cancelled the order'}), 200)
        return make_response(jsonify({'message': 'Failed to cancel order'}), 400)

