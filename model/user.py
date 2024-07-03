from datetime import datetime
from typing import Union

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship

from model.base import Base
from model.rental import Rental

class User(Base):
    __tablename__ = 'user'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    driver_license_number = Column(String, unique=True)
    date_added = Column(DateTime, default=datetime.now())
    
    rentals = relationship("Rental", back_populates="user")
    
    def __init__(
        self, 
        name: str, 
        email: str, 
        password: str, 
        driver_license_number: str, 
        date_added: Union[DateTime, None] = None
    ):
        """
        Initialize a User instance.

        Args:
            name (str): The name of the user.
            email (str): The email address of the user. Must be unique.
            password (str): The password for the user account.
            driver_license_number (str): The driver's license number of the user. Must be unique.
            date_added (Union[DateTime, None], optional): The date the user was added. Defaults to None.
        """
        self.name = name
        self.email = email
        self.password = password
        self.driver_license_number = driver_license_number

        if date_added:
            self.date_added = date_added
    
    def add_rental(self, rental: Rental):
        """
        Add a rental to the user.

        Args:
            rental (Rental): The rental to add.
        """
        self.rentals.append(rental)
