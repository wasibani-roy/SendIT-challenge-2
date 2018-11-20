from flask import jsonify, make_response, request
from app.helper import validate_not_username_string, validate_no_data \
    , validate_not_username_characters
from .models import User
import flask.views
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token


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

        if validate_not_username_string(username):
            return make_response(jsonify({"Message": "Username must be a string"}), 400)
        if validate_no_data(username):
            return make_response(jsonify({"Message": "Username is required"}), 400)
        if validate_no_data(password):
            return make_response(jsonify({"Message": "Password is required"}), 400)
        if validate_not_username_characters(username):
            return make_response(jsonify({"Message": "Username must contain only characters"}), 400)

        # read from database to find the user and then check the password

        user = existing_user.fetch_user(username)
        if user and check_password_hash(user['password'], password):
            access_token = create_access_token\
                (identity={"user_id": user['user_id'], "username": user['username']})
            return make_response(jsonify({
                "message": "You have successfully logged in {}".format(user['username']),
                "access token": access_token}), 200)

        return make_response(jsonify({'message': 'Invalid credentials'}), 401)
