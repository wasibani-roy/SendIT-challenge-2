"""This module handles all data requests coming from controllers"""
import psycopg2
from app.database import Database

DB = Database()


class User:
    """This class handles database transactions for the user"""

    def __init__(self, username, email, password, role):
        """Constructor to intialise our class"""
        self.username = username
        self.email = email
        self.password = password
        self.role = role

    def insert_user_data(self):
        """Method to insert user data into our table"""
        try:
            query = "INSERT INTO users (username,password,email,role) VALUES(%s, %s,%s,%s)"
            data = (self.username, self.password, self.email, self.role)
            user = DB.cur.execute(query, data)
            return {'message': 'user registered succesfully'}, 201
        except Exception as error:
            raise error

    def fetch_user(self, username):
        """Method to fetch a given users data by name"""
        try:
            query = "SELECT * FROM users WHERE username=%s"
            DB.cur.execute(query, (username,))
            user = DB.cur.fetchone()
            return user
        except:
            return {'message': 'user not found'}, 404

    def check_user(self, username):
        """Method to check if a give user already exists in the database"""
        query = "SELECT * FROM users WHERE username=%s"
        DB.cur.execute(query, (username,))
        user = DB.cur.fetchone()
        if user:
            return True
        return False

    def fetch_all_users(self):
        """ Fetches all user records from the database"""
        try:
            query = ("SELECT * FROM users;")
            DB.cur.execute(query)
            rows = DB.cur.fetchall()
            return rows
        except (Exception, psycopg2.DatabaseError)as error:
            raise error

    @staticmethod
    def fetch_user_by_id(user_id):
        """Method to fetch user data by user id"""
        try:
            query = "SELECT * FROM users WHERE user_id=%s"
            DB.cur.execute(query, (user_id,))
            user = DB.cur.fetchone()
            return user
        except:
            return {'message': 'user not found'}, 404


