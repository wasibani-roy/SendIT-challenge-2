"""This module handles the data of parcel routes"""
from app.database import Database

db = Database()


class Order:
    """ Class for modeling orders """

    def __init__(self, order_id, user_id, parcel_name,
                 receiver_name, destination, status, present_location,
                 deliver_status, price):
        """
            This method acts as a constructor
            for our class, its used to initialise class attributes
        """
        self.user_id = user_id
        self.order_id = order_id
        self.parcel_name = parcel_name
        self.receiver_name = receiver_name
        self.destination = destination
        self.present_location = present_location
        self.status = status
        self.deliver_status = deliver_status
        self.price = price

    def insert_order_data(self):
        """
            This method inserts data into the orders tables
        """
        try:
            query = "INSERT INTO orders (user_id,parcel_name,receiver_name,destination,\
           location,status,deliver_status,price)\
             VALUES(%s,%s,%s,%s,%s,%s,%s,%s)"
            data = (self.user_id, self.parcel_name,
                    self.receiver_name, self.destination,
                    self.present_location, self.status, self.deliver_status,self.price)
            db.cur.execute(query, data)
            return True
        except Exception as error:
            raise error

    def user_orders(self):
        """This method is used to pick all the orders for a given user and return them"""
        query = """SELECT  * from orders where orders.user_id = %s"""
        db.cur.execute(query, (self.user_id,))
        user_order = db.cur.fetchall()
        return user_order

    def single_order(self):
        """This method is used to pick a specific order for a given user"""
        query = """SELECT  * FROM orders WHERE orders.user_id = %s AND parcel_order_id = %s"""
        db.cur.execute(query, (self.user_id, self.order_id))
        user_order = db.cur.fetchone()
        return user_order

    @staticmethod
    def order_history():
        """This method gets all parcel orders made and returns them"""
        query = "select users.username, orders.parcel_name, orders.destination, orders.status,\
         orders.receiver_name, orders.price, orders.location, orders.parcel_order_id,orders.deliver_status\
          from orders join users on orders.user_id=users.user_id"
        db.cur.execute(query)
        rows = db.cur.fetchall()
        return rows

    def fetch_user_by_id(self):
        """This method returns a specific users details basing on user id"""
        try:
            query = "SELECT * FROM users WHERE user_id=%s"
            db.cur.execute(query, (self.user_id,))
            user = db.cur.fetchone()
            return user
        except Exception as error:
            return error

    @staticmethod
    def fetch_role(user_id):
        """Method to fetch user role by user id"""
        query = "SELECT * FROM users WHERE user_id=%s"
        db.cur.execute(query, (user_id,))
        user = db.cur.fetchone()
        return user["role"]

    def update_delivery_status(self):
        """This method updates the delivery status of a specific parcel order"""
        query = "UPDATE orders SET deliver_status = %s WHERE parcel_order_id = %s"
        db.cur.execute(query, (self.deliver_status, self.order_id,))
        updated_rows = db.cur.rowcount
        return updated_rows

    def check_delivery_status(self):
        """This method checks the delivery status of a parcel order"""
        query = "SELECT deliver_status FROM orders WHERE parcel_order_id = %s"
        db.cur.execute(query, (self.order_id,))
        orders = db.cur.fetchone()
        if orders["deliver_status"] == "delivered":
            return True

    def update_destination(self):
        """This method is used to update the destination of a parcel"""
        query = "UPDATE orders SET destination = %s WHERE parcel_order_id = %s and user_id=%s"
        db.cur.execute(query, (self.destination, self.order_id, self.user_id))
        updated_rows = db.cur.rowcount
        return updated_rows

    def update_present_location(self):
        """This method updates location of the parcel"""
        query = "UPDATE orders SET location = %s WHERE parcel_order_id = %s"
        db.cur.execute(query, (self.present_location, self.order_id,))
        updated_rows = db.cur.rowcount
        return updated_rows

    def fetch_parcel_name(self):
        """This methods picks a specific parcel order for a user"""
        query = "SELECT * FROM orders WHERE parcel_name=%s AND user_id=%s"
        db.cur.execute(query, (self.parcel_name, self.user_id,))
        orders = db.cur.fetchone()
        return orders
