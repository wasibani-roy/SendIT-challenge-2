"""This module handles the login route"""
from flask import jsonify, make_response, request
import flask.views
from flask_jwt_extended import create_access_token
from flasgger import swag_from
from werkzeug.security import check_password_hash
from app.helper import (is_not_valid_username, is_not_valid_password, validate_not_keys)
from .models import User




class Login(flask.views.MethodView):
    """class function for post route URL"""

    @swag_from('../docs/login.yml', methods=['POST'])
    def post(self):
        """
        Allows users to login to their accounts

        """
        data = request.get_json()
        if validate_not_keys(data, 3):
            return make_response(jsonify({"message": "Some fields are missing!"}), 400)
        username = data.get('username')
        password = data.get('password')
        role = data.get('role')
        existing_user = User(username=username.lower(), email="none", password=password, role="none")

        if is_not_valid_username(username.strip()):
            return make_response(jsonify({"message": "Username is incorrect"}), 400)
        if is_not_valid_password(password.strip()):
            return make_response(jsonify({"message": "Password is incorrect"}), 400)


        # read from database to find the user and then check the password

        user = existing_user.fetch_user(username)
        if user and check_password_hash(user['password'], password):
            access_token = create_access_token \
                (identity={"user_id": user['user_id']})
            return make_response(jsonify({
                "message": "You have successfully logged in",
                "access token": access_token}), 200)

        return make_response(jsonify({'message': 'Invalid credentials'}), 401)
