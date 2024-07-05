from datetime import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Numeric
from sqlalchemy.orm import relationship

from model import Base

class Car(Base):
    __tablename__ = 'car'

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, nullable=False)
    model = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    price_per_day = Column(Numeric(10, 2), nullable=False)
    availability_status = Column(Boolean, default=True, nullable=False)
    date_added = Column(DateTime, default=datetime.now)

    rentals = relationship("Rental", back_populates="car")

    def __init__(
        self, 
        make: str, 
        model: str, 
        year: int, 
        price_per_day: float, 
        availability_status: bool = True, 
        date_added: Optional[datetime] = None
    ):
        """
        Initialize a Car instance.

        Args:
            make (str): The make of the car (e.g., Toyota, Ford).
            model (str): The model of the car (e.g., Camry, Focus).
            year (int): The year the car was manufactured.
            price_per_day (float): The rental price per day in currency units.
            availability_status (bool): The availability status of the car for rental (default is True).
            date_added (Optional[datetime]): The date and time when the car was added to the database.
        """
        self.make = make
        self.model = model
        self.year = year
        self.price_per_day = price_per_day
        self.availability_status = availability_status
        self.date_added = date_added if date_added else datetime.now()
        