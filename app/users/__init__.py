from .views import UserRegistration, UserLogin
from flask import Blueprint

users = Blueprint('user_data',__name__, url_prefix='/api/v1')

users.add_url_rule('/signup', view_func=UserRegistration.as_view('register user'),
                    methods=['POST'], strict_slashes=False)
users.add_url_rule('/signup', view_func=UserRegistration.as_view('get user'),
                    methods=['GET'], strict_slashes=False)
users.add_url_rule('/login', view_func=UserLogin.as_view('login user'),
                    methods=['POST'], strict_slashes=False)