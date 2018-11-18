import re


def validate_no_data(key):
    if not key or key.isspace():
        return True


def validate_data_not_length(key):
    if len(str(key)) < 4:
        return True


def validate_not_username_string(key):
    if not isinstance(key, str):
        return True
def validate_not_order_detail_string(key):
    if not isinstance(key, str):
        return True


def validate_not_username_characters(key):
    if not re.compile('^[a-zA-Z]+$').match(key):
        return True
def validate_not_order_detail_characters(key):
    if not re.compile('^[a-zA-Z]+$').match(key):
        return True


def validate_not_email(key):
    if '@' and '.' not in key:
        return True


def validate_not_email_structure(key):
    if key[0] == '@' or key[0] == '.' and key.index("@") >= key.index('.') and key.count("@") > 1 or key.count(".") > 1:
        return True
