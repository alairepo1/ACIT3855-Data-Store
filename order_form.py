from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime

class OrderForm(Base):
    """Class for order form"""

    __tablename__ = "order_form"

    id = Column(Integer, primary_key=True)
    customer_address= Column(String(250), nullable=False)
    customer_id= Column(String(250), nullable=False)
    customer_name= Column(String(50), nullable=False)
    price_id= Column(Integer, nullable=False)
    shoe_id= Column(String(100), nullable=False)
    timestamp= Column(String(100), nullable=False)
    date_created= Column(String(100), nullable=False)


    def __init__(self, customer_address, customer_id, customer_name, price_id, shoe_id, timestamp):
        """Initializes order form """
        self.customer_address = customer_address
        self.customer_id = customer_id
        self.customer_name = customer_name
        self.price_id = price_id
        self.shoe_id = shoe_id
        self.timestamp = timestamp
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary represnation of the order form"""
        dict = {}
        dict["id"] = self.id
        dict['customer_address'] = self.customer_address
        dict['customer_id'] = self.customer_id
        dict['customer_name'] = self.customer_name
        dict['price'] = self.price_id
        dict['shoe_id'] = self.shoe_id
        dict['timestamp'] = self.timestamp
        dict['date_created'] = self.date_created

        return dict