from flask import Flask, jsonify
from instance.config import app_config
from flask_jwt_extended import JWTManager
from .users import users as users_blueprint
from .parcel import orders as orders_blueprint
from flasgger import Swagger


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    Swagger(app)

    """We add JWT secret key constant"""
    app.config["JWT_SECRET_KEY"] = "wasibani93-256"

    """   
     initialize jwt by passing our app instance to JWTManager class.

    """
    jwt = JWTManager(app)

    """
    Registering blueprints

    """

    app.register_blueprint(users_blueprint)


    app.register_blueprint(orders_blueprint)


    @app.errorhandler(405)
    def url_not_found(error):
        return jsonify({'message': 'requested url is invalid'}), 405

    @app.errorhandler(404)
    def content_not_found(error):
        return jsonify({'message': 'requested url is not found'}), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({'message': 'internal server error'}), 500

    @app.errorhandler(500)
    def duplicate_keys(error):
        return jsonify({'message': 'internal server error'}), 500

    @app.route('/')
    def index():
        return "Welcome to sendIT application"

    return app


