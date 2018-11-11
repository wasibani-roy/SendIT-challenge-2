"""
    Global variable users_data  holds  user data , initially its empty
"""

users_data = []

class User:
    def __init__(self, user_name, email, password):
        """
            This method acts as a constructor
            for our class, its used to initialise class attributes
        """
        if len(users_data) == 0:
            user_id = len(users_data) + 1
        user_id = len(users_data) + 1
        self.user_id = user_id
        self.user_name = user_name
        self.email = email
        self.password = password

    def create_user(self):
        """
            This method receives an object of the
            class, creates and returns a dictionary from the object
        """
        user = {
            "user_id" :self.user_id,
            "user_name" : self.user_name,
            "email" : self.email,
            "password" : self.password
        }

        users_data.append(user)
        return user
    @staticmethod
    def get_user_id(user_name):
        for existing_user in users_data:
            if user_name == existing_user['user_name']:
                return existing_user['user_id']
        return {"message": "user doesn't exist"}

