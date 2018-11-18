# post_an_order = {
#     "parcel_name": "wardrobe",
#     "destination": "mutundwe",
#     "username": "wasibani",
#     "receiver": "danny1",
#     "user_id":1
#
# }
# post_an_order_no_username = {
#     "parcel_name": "wardrobe",
#     "destination": "mutundwe",
#     "receiver": "danny1",
#     "user_id":1
#
# }
# post_an_order_no_parcelname = {
#     "destination": "mutundwe",
#     "username": "wasibani",
#     "receiver": "danny1",
#     "user_id":1
#
# }
# post_with_empty_destination = {
#     "parcel_name": "roy 234",
#     "username": "wasibani",
#     "receiver": "danny",
#     "destination": "",
#     "present_location": "wandegeya",
#     "status": "pending"
# }
user_register_data = {
    "username": "wasibani",
    "email": "roy@me.com",
    "password": "12345"
}
admin_register_data = {
    "username": "admin",
    "email": "admin@me.com",
    "password": "admin"
}
user_register_data_invalid_email = {
    "username": "wasibani",
    "email": "",
    "password": "12345"
}
user_register_data_invalid_email_structure = {
    "username": "wasibani",
    "email": "roymecom",
    "password": "12345"
}
user_register_data_invalid_email_structure2 = {
    "username": "wasibani",
    "email": "@royme.com",
    "password": "12345"
}
user_register_data_invalid_username_len = {
    "username": "roy",
    "email": "roy@me.com",
    "password": "12345"
}
user_register_data_invalid_password = {
    "username": "wasibani",
    "email": "roy@me.com",
    "password": ""
}
user_register_data_invalid_password_len = {
    "username": "wasibani",
    "email": "roy@me.com",
    "password": "roy"
}
user_register_data_invalid_username = {
    "username": "",
    "email": "roy@me.com",
    "password": "12345"
}
user_login_data = {
    "username": "wasibani",
    "password": "12345"
}
admin_login_data = {
    "username": "wasibani",
    "password": "12345"
}
user_login_data_invalid_password = {
    "username": "wasibani",
    "password": "wasiba"
}
user_login_data_invalid_username = {
    "password": "12345"
}
user_login_data_invalid_name = {
    "username": "Danny12",
    "password": "12345"
}

