from instance.config import app_config
from flask import Flask, jsonify


def create_app(config_name):

    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    app.secret_key = "SendIT"
    # app.config.from_pyfile('config.py')

    """
    registering Blueprints

    """
    from app.parcel_order import orders as orders_blueprints
    app.register_blueprint(orders_blueprints)

    from app.users import users as users_blueprints
    app.register_blueprint(users_blueprints)

    @app.errorhandler(405)
    def url_not_found(error):
        return jsonify({'message':'requested url is invalid'}), 405

    @app.errorhandler(404)
    def content_not_found(error):
        return jsonify({'message':'requested url is not found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'message':'internal server error'}), 500



    @app.route('/')
    def index():
        return "SendIT"
    return app
