from flask import jsonify, make_response, request
from .models import User
import flask.views
from werkzeug.security import generate_password_hash
from app.helper import *

class Register(flask.views.MethodView):

    def post(self):
        try:
            parser = request.get_json()
            username = parser.get('username')
            user_password = parser.get('password')
            email = parser.get('email')
            password = generate_password_hash(
                user_password, method='sha256')

            if validate_not_username_string(username):
                return make_response(jsonify({"Message":"Username must be a string"}), 400)
            if validate_no_data(username):
                return make_response(jsonify({"Message":"Username is required"}), 400)
            if validate_no_data(user_password):
                return make_response(jsonify({"Message":"Password is required"}), 400)
            if validate_not_username_characters(username):
                return make_response(jsonify({"Message":"Username must contain only characters"}), 400)
            if validate_no_data(email):
                return make_response(jsonify({"Message":"email is required"}), 400)
            if validate_data_not_length(username):
                return make_response(jsonify({"Message":"username is to short"}), 400)
            if validate_data_not_length(user_password):
                return make_response(jsonify({"Message":"password is to short"}), 400)
            if validate_not_email(email):
                return make_response(jsonify({"Message":"please input a valid email"}), 400)
            if validate_not_email_structure(email):
                return make_response(jsonify({"Message":"please input valid email"}), 400)

            """creating an instance of the user class"""
            use = User(username.lower(), email, password)
            user = use.check_user(username)
            if user:
                return make_response(jsonify({'Message': 'Username already exists'}), 403)
            use.insert_user_data()
            return make_response(jsonify({'Message': "you have succesfully signed up"}), 201)
        except Exception as e:
            raise e
