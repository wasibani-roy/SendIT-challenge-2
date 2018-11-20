from flask import jsonify, make_response
from app.helper import validate_no_data, validate_not_order_detail_string
from .models import Order
from flask import request
import flask.views
from flask_jwt_extended import jwt_required, get_jwt_identity

class UserSpecificOrder(flask.views.MethodView):
    @jwt_required
    def get(self):
        """Method handling the get a specific users parcel orders"""
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        new_order = Order(user_id=user_id, parcel_name=None, order_id=None, receiver_name=None, status=None,
                          deliver_status=None \
                          , destination=None, present_location=None)
        order = new_order.user_orders()
        if not order:
            return make_response(jsonify({'messege': "you have no orders at this time"}), 404)
        return make_response(jsonify({'orders': order}), 200)

    @jwt_required
    def put(self, parcel_id):
        """Method handling the update of destination"""
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        parser = request.get_json()
        destination = parser.get('destination')
        order = Order(user_id=user_id, parcel_name=None, order_id=parcel_id, \
                      receiver_name=None, status=None,
                      deliver_status=None \
                      , destination=destination.lower(), present_location=None)
        if validate_not_order_detail_string(destination):
            return make_response(jsonify({'Message': 'Destination must be a string'}), 400)
        if validate_no_data(destination):
            return make_response(jsonify({'Message': 'Please enter the new destination'}), 400)
        if order.check_delivery_status():
            return make_response(jsonify({"Message": "You can not change the destination of a delivered product"}), 400)

        update_destination = order.update_destination()
        if update_destination:
            return make_response(jsonify({'Message': 'destination updated succesfully'}), 200)
        return make_response(jsonify({'Message': 'Failed to update destination'}), 400)


class UserSpecificOrderById(flask.views.MethodView):
    @jwt_required
    def get(self, parcel_id):
        """Method handling the get a specific users parcel order by id"""
        current_user = get_jwt_identity()
        user_id = current_user['user_id']
        new_order = Order(user_id=user_id, parcel_name=None, order_id=parcel_id, receiver_name=None, status=None,
                          deliver_status=None \
                          , destination=None, present_location=None)
        order = new_order.single_order()
        if not order:
            return make_response(jsonify({'Messege': "This parcel order doesn't exist please check id and try again"}),
                                 404)
        return make_response(jsonify({'orders': order}), 200)
