from datetime import datetime, date
from typing import Optional

from sqlalchemy import Column, Integer, Date, DateTime, Numeric, ForeignKey
from sqlalchemy.orm import relationship

from model.base import Base

class Rental(Base):
    __tablename__ = 'rental'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    car_id = Column(Integer, ForeignKey('car.id'), nullable=False)
    rental_start_date = Column(Date, nullable=False)
    rental_end_date = Column(Date, nullable=False)
    total_price = Column(Numeric(10, 2), nullable=False)
    date_added = Column(DateTime, default=datetime.now)

    user = relationship("User", back_populates="rentals")
    car = relationship("Car", back_populates="rentals")

    def __init__(
        self, 
        user_id: int, 
        car_id: int, 
        rental_start_date: date, 
        rental_end_date: date, 
        total_price: float, 
        date_added: Optional[datetime] = None
    ):
        self.user_id = user_id
        self.car_id = car_id
        self.rental_start_date = rental_start_date
        self.rental_end_date = rental_end_date
        self.total_price = total_price
        self.date_added = date_added if date_added else datetime.now()