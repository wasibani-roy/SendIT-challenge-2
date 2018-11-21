"""This module handles the login route"""
from flask import jsonify, make_response, request
import flask.views
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from app.helper import (is_not_valid_username, is_not_valid_password)
from .models import User




class Login(flask.views.MethodView):
    """class function for post route URL"""

    def post(self):
        """
        Allows users to login to their accounts

        """
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        existing_user = User(username=username.lower(), email="none", password=password)

        if is_not_valid_username(username.strip()):
            return make_response(jsonify({"Message": "Username is incorrect"}), 400)
        if is_not_valid_password(password.strip()):
            return make_response(jsonify({"Message": "Password is incorrect"}), 400)


        # read from database to find the user and then check the password

        user = existing_user.fetch_user(username)
        if user and check_password_hash(user['password'], password):
            access_token = create_access_token \
                (identity={"user_id": user['user_id'], "username": user['username']})
            return make_response(jsonify({
                "message": "You have successfully logged in {}".format(user['username']),
                "access token": access_token}), 200)

        return make_response(jsonify({'message': 'Invalid credentials'}), 401)
