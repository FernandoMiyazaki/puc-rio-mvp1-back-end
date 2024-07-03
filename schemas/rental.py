from pydantic import BaseModel
from typing import List
from datetime import date
from model.rental import Rental

class RentalSchema(BaseModel):
    """
    Schema representing the basic details of a rental.

    Attributes:
        user_id (int): The ID of the user who is renting the car.
        car_id (int): The ID of the car being rented.
        rental_start_date (date): The start date of the rental period.
        rental_end_date (date): The end date of the rental period.
        total_price (float): The total price of the rental.
    """
    user_id: int
    car_id: int
    rental_start_date: date
    rental_end_date: date
    total_price: float

class RentalSearchSchema(BaseModel):
    """
    Defines how the structure representing a search should be.
    The search will be made based only on the rental's ID.
    """
    id: int = 1

class RentalViewSchema(RentalSchema):
    """
    Schema representing a detailed view of a rental including its ID.

    Attributes:
        id (int): The unique identifier of the rental.
    """
    id: int = 1
    user_id: int = 1
    car_id: int = 1
    rental_start_date: date = date.today()
    rental_end_date: date = date.today()
    total_price: float = 0.0

class RentalListSchema(BaseModel):
    """
    Schema representing a list of rentals.

    Attributes:
        rentals (List[RentalViewSchema]): A list of rental details.
    """
    rentals: List[RentalViewSchema]

def present_rentals(rentals: List[Rental]):
    """
    Returns a representation of the rentals following the schema defined in RentalViewSchema.

    Args:
        rentals (List[Rental]): A list of rental objects.

    Returns:
        dict: A dictionary with a list of rental details.
    """
    result = []
    for rental in rentals:
        result.append({
            "id": rental.id,
            "user_id": rental.user_id,
            "car_id": rental.car_id,
            "rental_start_date": rental.rental_start_date,
            "rental_end_date": rental.rental_end_date,
            "total_price": rental.total_price
        })
    return {"rentals": result}

class RentalDeleteSchema(BaseModel):
    """
    Defines how the data structure returned after a delete request should be.

    Attributes:
        message (str): The message indicating the result of the deletion.
        id (int): The ID of the rental that was deleted.
    """
    message: str
    id: int

def present_rental(rental: Rental):
    """
    Returns a representation of the rental following the schema defined in RentalViewSchema.

    Args:
        rental (Rental): A rental object.

    Returns:
        dict: A dictionary with the rental details.
    """
    return {
        "id": rental.id,
        "user_id": rental.user_id,
        "car_id": rental.car_id,
        "rental_start_date": rental.rental_start_date,
        "rental_end_date": rental.rental_end_date,
        "total_price": rental.total_price
    }