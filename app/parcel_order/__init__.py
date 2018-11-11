from flask import Blueprint
from .views import OrdersList, SingleOrder, UserOrder


orders = Blueprint("parcel_orders", __name__, url_prefix='/api/v1')

orders.add_url_rule('/parcels', view_func=OrdersList.as_view('post parcel'),
                    methods=['POST'], strict_slashes=False)
orders.add_url_rule('/parcels', view_func=OrdersList.as_view('get parcel'),
                    methods=['GET'], strict_slashes=False)
orders.add_url_rule('/parcels/<int:parcel_id>', view_func=SingleOrder.as_view('get specific'),
                    methods=['GET'], strict_slashes=False)
orders.add_url_rule('/parcels/<int:parcel_id>/cancel', view_func=SingleOrder.as_view('cancel order'),
                    methods=['PUT'], strict_slashes=False)
orders.add_url_rule('/users/<int:user_id>/parcels', view_func=UserOrder.as_view('user parcel'),
                    methods=['GET'], strict_slashes=False)
