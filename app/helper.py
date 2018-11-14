import flask, functools
from flask import jsonify, make_response


def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        else:
            return make_response(jsonify({"message": "Please log in to access this resource"}), 401)

    return wrapper


def validate_data(key):
    if not key or key.isspace():
        return True

def validate_data_length(key):
    if len(str(key)) < 4:
        return True
