import flask, functools
from flask import jsonify, make_response


def login_required(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        if 'username' in flask.session:
            return method(*args, **kwargs)
        else:
            flask.flash("A login is required to see the page!")
            return make_response(jsonify({"message": "Please log in to access this resource"}), 400)
    return wrapper