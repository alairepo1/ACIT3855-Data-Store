from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class RepairForm(Base):
    """Class for Repair forms"""

    __tablename__ = "repair_form"

    id = Column(Integer, primary_key=True)
    customer_address= Column(String(250), nullable=False)
    customer_id= Column(String(250), nullable=False)
    customer_name= Column(String(50), nullable=False)
    damage_description= Column(String(500), nullable=False)
    shoe_type= Column(String(250), nullable=False)
    timestamp= Column(String(100), nullable=False)
    date_created= Column(String(100), nullable=False)

    def __init__(self, customer_address, customer_id, customer_name, damage_description, shoe_type, timestamp):
        """Initializes order form """
        self.customer_address = customer_address
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.damage_description = damage_description
        self.shoe_type = shoe_type
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary represnation of the order form"""
        dict = {}
        dict["id"] = self.id
        dict['customer_address'] = self.customer_address
        dict['customer_id'] = self.customer_id
        dict['customer_name'] = self.customer_name
        dict['damage_description'] = self.damage_description
        dict['shoe_type'] = self.shoe_type
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created

        return dict