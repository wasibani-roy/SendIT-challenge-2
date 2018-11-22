"""This files handles validation of input data"""
import re


# def validate_no_data(key):
#     if not key or key.isspace():
#         return True
#
#
# def validate_data_not_length(key):
#     if len(str(key)) < 4:
#         return True

def is_not_valid_username(key):
    """This method validates the users username"""
    if not key or key.isspace() or not re.compile('^[a-zA-Z]+$').match(key) \
            or not len(str(key)) > 4 or not isinstance(key, str):
        return True


def is_not_valid_role(key):
    """This method validates the users role"""
    if not key or key.isspace() or not re.compile('^[a-zA-Z]+$').match(key) \
            or not isinstance(key, str):
        return True


def is_not_valid_password(key):
    """This method checks to see a password has been entered"""
    if not key or key.isspace() or len(str(key)) < 4:
        return True


# def validate_not_username_string(key):
#     if not isinstance(key, str):
#         return True
def is_not_valid_order(key):
    """This method validates order data sent by user"""
    if not key or key.isspace() or not isinstance(key, str) or not re.compile('^[a-zA-Z]+$').match(key):
        return True


# def validate_not_username_characters(key):
#     if not re.compile('^[a-zA-Z]+$').match(key):
#         return True
# def validate_not_order_detail_characters(key):
#     if not re.compile('^[a-zA-Z]+$').match(key):
#         return True


# def validate_not_email(key):
#     if '@' and '.' not in key:
#         return True


def validate_not_email_structure(key):
    """This method validates the email entered by user"""
    if '@' not in key or '.' not in key or key[0] == '@' or key[0] == '.' or key.index("@") >= key.index('.') \
            or key.count("@") > 1 \
            or key.count(".") > 1 or key.index(".") == key.index("@") + 1:
        return True
