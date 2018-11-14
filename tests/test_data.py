post_an_order = {
    "parcel_name": "wardrobe",
    "destination": "mutundwe",
    "username": "wasibani",
    "receiver": "danny1",
    "user_id":1

}
post_an_order_no_username = {
    "parcel_name": "wardrobe",
    "destination": "mutundwe",
    "receiver": "danny1",
    "user_id":1

}
post_an_order_no_parcelname = {
    "destination": "mutundwe",
    "username": "wasibani",
    "receiver": "danny1",
    "user_id":1

}
post_with_empty_destination = {
    "parcel_name": "roy 234",
    "username": "wasibani",
    "receiver": "danny",
    "destination": "",
    "present_location": "wandegeya",
    "status": "pending"
}
user_register_data = {
    "user_name": "wasibani",
    "email": "roy@me.com",
    "password": "12345"
}
user_register_data_invalid_email = {
    "user_name": "wasibani",
    "email": "",
    "password": "12345"
}
user_register_data_invalid_username_len = {
    "user_name": "roy",
    "email": "roy@me.com",
    "password": "12345"
}
user_register_data_invalid_password = {
    "user_name": "wasibani",
    "email": "roy@me.com",
    "password": ""
}
user_register_data_invalid_password_len = {
    "user_name": "wasibani",
    "email": "roy@me.com",
    "password": "roy"
}
user_register_data_invalid_username = {
    "user_name": "",
    "email": "roy@me.com",
    "password": "12345"
}
user_login_data = {
    "user_name": "wasibani",
    "password": "12345"
}
user_login_data_invalid_password = {
    "user_name": "wasibani",
}
user_login_data_invalid_username = {
    "password": "12345"
}
user_login_data_invalid_name = {
    "user_name": "Danny12",
    "password": "12345"
}
user_action_data = {
    "user_action": "cancel"
}
user_action_data_invalid_action = {
    "user_action": "send"
}
user_action_data_no_action = {

}
