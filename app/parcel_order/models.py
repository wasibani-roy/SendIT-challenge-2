from app.parcel.models import Parcel

""" 
    Global variable list  holds  orders , initially its empty

"""
orders_db = []


class Order(Parcel):
    """ Class for modeling orders """

    def __init__(self, parcel_order_id, user_id, user_name, receiver_name, parcel_name, destination, present_location,
                 status):
        """
            This method acts as a constructor
            for our class, its used to initialise class attributes
        """
        Parcel.__init__(self, parcel_name, destination)
        self.parcel_order_id = parcel_order_id
        self.user_id = user_id
        self.user_name = user_name
        self.receiver = receiver_name
        self.present_location = present_location
        self.status = status
        self.action = None

    def place_an_order(self):
        """
            This method receives an object of the
            class, creates and returns a dictionary from the object
        """
        parcel_order = {

            "parcel_order_id": self.parcel_order_id,
            "user_id": self.user_id,
            "parcel_name": self.parcel_name,
            "receiver": self.receiver,
            "parcel_destination": self.destination,
            "present_location": self.present_location,
            "status": self.status,
            "action": self.action

        }

        orders_db.append(parcel_order)
        return parcel_order
