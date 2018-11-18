from app.database import Database


db = Database()


class Order:
    """ Class for modeling orders """

    def __init__(self, order_id, user_id, parcel_name, receiver_name, destination, status, present_location, deliver_status):
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

    def insert_order_data(self):
        """
            This method inserts data into the orders tables
        """
        try:
            query = "INSERT INTO orders (user_id,parcel_name,receiver_name,destination,present_location,status,deliver_status) VALUES(%s,%s,%s,%s,%s,%s,%s)"
            data = (self.user_id, self.parcel_name,
                    self.receiver_name, self.destination, self.present_location, self.status, self.deliver_status)
            db.cur.execute(query, data)
            return True
        except Exception as e:
            raise e

    def user_orders(self):
        query = """SELECT  * from orders where orders.user_id = %s"""
        db.cur.execute(query, (self.user_id,))
        user_order = db.cur.fetchall()
        return user_order

    def single_order(self):
        query = """SELECT  * FROM orders WHERE orders.user_id = %s AND parcel_order_id = %s"""
        db.cur.execute(query, (self.user_id, self.order_id))
        user_order = db.cur.fetchone()
        return user_order

    @staticmethod
    def order_history():
        query = "select users.username, orders.parcel_name, orders.destination, orders.status,\
         orders.receiver_name, orders.present_location, orders.deliver_status from orders join users on orders.user_id=users.user_id"
        db.cur.execute(query)
        rows = db.cur.fetchall()
        return rows



    def fetch_user_by_id(self):
        try:
            query = "SELECT * FROM users WHERE user_id=%s"
            db.cur.execute(query, (self.user_id,))
            user = db.cur.fetchone()
            return user
        except Exception as e:
            return {'msg': 'user not found'}, 404


    def update_delivery_status(self):
        query = "UPDATE orders SET deliver_status = %s WHERE parcel_order_id = %s"
        db.cur.execute(query, (self.deliver_status, self.order_id,))
        updated_rows = db.cur.rowcount
        return updated_rows

    def check_delivery_status(self):
        query = "SELECT deliver_status FROM orders WHERE parcel_order_id = %s"
        db.cur.execute(query, (self.order_id,))
        orders = db.cur.fetchone()
        if orders["deliver_status"] == "delivered":
            return True

    def update_destination(self):
        query = "UPDATE orders SET destination = %s WHERE parcel_order_id = %s and user_id=%s"
        db.cur.execute(query, (self.destination, self.order_id, self.user_id))
        updated_rows = db.cur.rowcount
        return updated_rows

    def update_present_location(self):
        query = "UPDATE orders SET present_location = %s WHERE parcel_order_id = %s"
        db.cur.execute(query, (self.present_location, self.order_id,))
        updated_rows = db.cur.rowcount
        return updated_rows

    def fetch_parcel_name(self):
        query = "SELECT * FROM orders WHERE parcel_name=%s AND user_id=%s"
        db.cur.execute(query, (self.parcel_name, self.user_id,))
        orders = db.cur.fetchone()
        return orders

