"""This module handles the signup route"""
from flask import jsonify, make_response, request
import flask.views
from werkzeug.security import generate_password_hash
from flasgger import swag_from
from app.helper import (is_not_valid_username,\
                        is_not_valid_password, validate_not_email_structure, is_not_valid_role)
from .models import User


class Register(flask.views.MethodView):
    """class function for post route URL"""
    @swag_from('../docs/signup.yml', methods=['POST'])
    def post(self):
        """Method handling the user signup route"""
        try:
            parser = request.get_json()
            if len(parser.keys()) != 4:
                return make_response(jsonify({"message": "Some fields are missing!"}),400)
            username = parser.get('username')
            user_password = parser.get('password')
            email = parser.get('email')
            role = parser.get('role')
            password = generate_password_hash(
                user_password, method='sha256')

            if is_not_valid_username(username.strip()):
                return make_response(jsonify({"message": "Please supply a username\
                 of 4 or more characters"}), 400)
            if is_not_valid_password(user_password.strip()):
                return make_response(jsonify({"message": "Password is incorrect"}), 400)
            if is_not_valid_role(role.strip()):
                return make_response(jsonify({"message": "role is incorrect"}), 400)
            if validate_not_email_structure(email.strip()):
                return make_response(jsonify({"message": "email is incorrect"}), 400)

            # creating an instance of the user class
            use = User(username.lower(), email, password, role)
            user = use.check_user(username)
            if user:
                return make_response(jsonify({'message': 'Username already exists'}), 403)
            use.insert_user_data()
            return make_response(jsonify({'message': "you have succesfully signed up"}), 201)
        except Exception as error:
            raise error
