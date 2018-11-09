"""
    Global variable parcel_items  holds  parcels data
"""

parcel_items = []

class Parcel:
    def __init__(self,  parcel_name, destination):
        """
            This method acts as a constructor
        """
        if len(parcel_items) == 0:
            parcel_id = len(parcel_items) + 1
        parcel_id = len(parcel_items) + 1

        self.parcel_id = parcel_id
        self.parcel_name = parcel_name
        self.destination = destination

    def create_parcelItems(self):

        item = {
            "parcel_id" :self.parcel_id,
            "parcel_name" : self.parcel_name,
            "destination" : self.destination
        }

        parcel_items.append(item)
        return item

