from flask import jsonify, make_response, request
from .models import User, users_data
import flask.views
from app.helper import validate_data, validate_data_length
from flask_jwt_extended import create_access_token


class UserRegistration(flask.views.MethodView):

    def get(self):
        """
             This method returns all orders created
        """
        if not users_data:
            return make_response(jsonify({"message": "No Registered users"}), 200)
        return make_response(jsonify({"orders": users_data}), 200)

    def post(self):
        parser = request.get_json()
        user_name = parser.get('user_name')
        email = parser.get('email')
        password = parser.get('password')

        if validate_data(user_name):
            return make_response(jsonify({'message': 'user_name field is required'}), 400)
        if validate_data(email):
            return make_response(jsonify({'message': 'Please add you,re user email'}), 400)
        if validate_data(password):
            return make_response(jsonify({'message': 'Please add you,re user password'}), 400)

        if validate_data_length(user_name):
            return make_response(jsonify({'message': 'username is to short'}), 400)
        if validate_data_length(password):
            return make_response(jsonify({'message': 'password is too short'}), 400)

        new_user = User(user_name, email, password)

        for existing_user in users_data:
            if user_name == existing_user['user_name']:
                return make_response(jsonify({"message": "username already exists"}), 400)
        new_user.create_user()
        return make_response(jsonify({"message": "You have successfully registered"}), 201)


class UserLogin(flask.views.MethodView):
    def post(self):
        parser = request.get_json()
        user_name = parser.get('user_name')
        password = parser.get('password')

        if validate_data(user_name):
            return make_response(jsonify({'message': 'user_name field is required'}), 400)

        if validate_data(password):
            return make_response(jsonify({'message': 'Please add your user password'}), 400)

        for existing_user in users_data:
            if user_name != existing_user['user_name']:
                if password != existing_user['password']:
                    return make_response(jsonify({"message": "username and password dont match"}), 400)
            if password == existing_user['password'] and user_name == existing_user["user_name"]:
                user_id = User.get_user_id(user_name)
                access_token = create_access_token(identity={"user_id": user_id, "user_name": user_name})
                return make_response(jsonify({
                    "message": "You have successfully logged in this is you're", "access token": access_token}), 200)

        return make_response(jsonify({"message": "incorrect username and password"}), 200)
