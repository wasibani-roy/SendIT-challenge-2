from flask import Blueprint

from .user import UserSpecificOrder, UserSpecificOrderById
from .admin import AdminOrderLocation, AdminOrderStatus
from .parcel import ParcelOrder

orders = Blueprint('parcel', __name__, url_prefix='/api/v2')

orders.add_url_rule('/parcels', view_func=ParcelOrder.as_view('make order'),
                    methods=['POST'], strict_slashes=False)
orders.add_url_rule('/parcels', view_func=ParcelOrder.as_view('get order'),
                    methods=['GET'], strict_slashes=False)
orders.add_url_rule('/parcels/user', view_func=UserSpecificOrder.as_view('view users orders'),
                    methods=['GET'], strict_slashes=False)
orders.add_url_rule('/parcels/user/<int:parcel_id>', view_func=UserSpecificOrderById.as_view('view specific user orders'),
                    methods=['GET'], strict_slashes=False)
orders.add_url_rule('/parcels/<int:parcel_id>/destination', view_func=UserSpecificOrder.as_view('change destination'),
                    methods=['PUT'], strict_slashes=False)
orders.add_url_rule('/parcels/<int:parcel_id>/status', view_func=AdminOrderStatus.as_view('update parcel delivery status'),
                    methods=['PUT'], strict_slashes=False)
orders.add_url_rule('/parcels/<int:parcel_id>/presentLocation', view_func=AdminOrderLocation.as_view('update parcel present location'),
                    methods=['PUT'], strict_slashes=False)


