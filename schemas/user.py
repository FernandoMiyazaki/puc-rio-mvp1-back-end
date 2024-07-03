from pydantic import BaseModel
from typing import Optional, List
from model.user import User
from schemas import RentalSchema

class UserSchema(BaseModel):
    """
    Defines how a new user to be inserted should be represented.
    """
    name: str = "John Doe"
    email: str = "john.doe@example.com"
    password: str = "password123"
    driver_license_number: str = "D12345678"

class UserSearchSchema(BaseModel):
    """
    Defines how the structure representing a search should be.
    The search will be made based only on the user's id.
    """
    id: int = 1

class UserListSchema(BaseModel):
    """
    Defines how a list of users will be returned.
    """
    users: List[UserSchema]

def present_users(users: List[User]):
    """
    Returns a representation of the users following the schema defined in UserSchema.
    """
    result = []
    for user in users:
        result.append({
            "name": user.name,
            "email": user.email,
            "password": user.password,
            "driver_license_number": user.driver_license_number
        })
    return {"users": result}

class UserViewSchema(BaseModel):
    """
    Defines how a user will be returned: user + rentals.
    """
    id: int = 1
    name: str = "John Doe"
    email: str = "john.doe@example.com"
    password: str = "password123"
    driver_license_number: str = "D12345678"
    total_rentals: int = 1
    rentals: List[RentalSchema]

class UserDeleteSchema(BaseModel):
    """
    Defines how the data structure returned after a delete request should be.
    """
    message: str
    email: str

def present_user(user: User):
    """
    Returns a representation of the user following the schema defined in UserViewSchema.
    """
    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "password": user.password,
        "driver_license_number": user.driver_license_number,
        "total_rentals": len(user.rentals),
        "rentals": [{"start_date": r.start_date, "end_date": r.end_date, "car_id": r.car_id} for r in user.rentals]
    }