from pydantic import BaseModel
from typing import Optional, List
from model.car import Car

class CarSchema(BaseModel):
    """
    Schema representing the basic details of a car.

    Attributes:
        make (str): The make of the car (e.g., Toyota, Ford).
        model (str): The model of the car (e.g., Camry, Focus).
        year (int): The year the car was manufactured.
        price_per_day (float): The rental price per day in currency units.
    """
    make: str = "Toyota"
    model: str = "Camry"
    year: int = 2020
    price_per_day: float = 45.00

class CarSearchSchema(BaseModel):
    """
    Defines how the structure representing a search should be.
    The search will be made based only on the car's model.
    """
    id: int = 1

class CarListSchema(BaseModel):
    """
    Schema representing a list of cars.

    Attributes:
        cars (List[CarSchema]): A list of car details.
    """
    cars: List[CarSchema]

def present_cars(cars: List[Car]):
    """
    Returns a representation of the cars following the schema defined in CarSchema.
    """
    result = []
    for car in cars:
        result.append({
            "id": car.id,
            "make": car.make,
            "model": car.model,
            "year": car.year,
            "price_per_day": car.price_per_day
        })
    return {"cars": result}

class CarViewSchema(BaseModel):
    """
    Schema representing a detailed view of a car including its ID and availability status.

    Attributes:
        id (int): The unique identifier of the car.
        make (str): The make of the car (e.g., Toyota, Ford).
        model (str): The model of the car (e.g., Camry, Focus).
        year (int): The year the car was manufactured.
        price_per_day (float): The rental price per day in currency units.
        availability_status (bool): The availability status of the car for rental.
    """
    id: int
    make: str = "Toyota"
    model: str = "Camry"
    year: int = 2020
    price_per_day: float = 45.00
    availability_status: bool = True

class CarDeleteSchema(BaseModel):
    """
    Defines how the data structure returned after a delete request should be.

    Attributes:
        message (str): The message indicating the result of the deletion.
        model (str): The model of the car that was deleted.
    """
    message: str
    model: str

def present_car(car: Car):
    """
    Returns a representation of the car following the schema defined in CarViewSchema.
    """
    return {
        "id": car.id,
        "make": car.make,
        "model": car.model,
        "year": car.year,
        "price_per_day": car.price_per_day,
        "availability_status": car.availability_status
    }