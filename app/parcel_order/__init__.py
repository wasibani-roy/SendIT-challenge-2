from flask import Blueprint
from .views import OrdersList, SingleOrder
from flask_restful import Api


orders = Blueprint("parcel_orders", __name__, url_prefix='/api/v1')

orders_api = Api(orders)
orders_api.add_resource(OrdersList, '/parcels')
orders_api.add_resource(SingleOrder, '/parcels/<int:order_id>')

