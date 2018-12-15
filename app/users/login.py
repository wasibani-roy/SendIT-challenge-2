"""This module handles the login route"""
from flask import jsonify, make_response, request
import flask.views
from flask_jwt_extended import create_access_token
from flasgger import swag_from
from werkzeug.security import check_password_hash
from app.helper import (is_not_valid_password, validate_not_keys,\
                        validate_not_email_structure)
from .models import User




class Login(flask.views.MethodView):
    """class function for post route URL"""

    @swag_from('../docs/login.yml', methods=['POST'])
    def post(self):
        """
        Allows users to login to their accounts

        """
        data = request.get_json()
        if validate_not_keys(data, 2):
            return make_response(jsonify({"message": "Some fields are missing!"}), 400)
        user_email = data.get('email')
        password = data.get('password')
        # username_actual = username.lower()
        existing_user = User(username=None, email=user_email, password=password, role=None)

        if validate_not_email_structure(user_email):
            return make_response(jsonify({"message": "email is incorrect"}), 400)
        if is_not_valid_password(password.strip()):
            return make_response(jsonify({"message": "Password is incorrect"}), 400)


        # read from database to find the user and then check the password

        user = existing_user.fetch_user(user_email)
        if user and check_password_hash(user['password'], password):
            access_token = create_access_token \
                (identity={"user_id": user['user_id'], "role": user['role']})
            return make_response(jsonify({
                "message": "You have successfully logged in",
                "access_token": access_token}), 200)

        return make_response(jsonify({'message': 'Invalid credentials'}), 401)
