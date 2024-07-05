import os

from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from flask_cors import CORS
from sqlalchemy.exc import IntegrityError

from model import Session, User, Car, Rental
from logger import logger
from schemas import *

info = Info(title="Car Rental API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

home_tag = Tag(name="Documentation", description="Selection of documentation: Swagger, Redoc, or RapiDoc")
user_tag = Tag(name="User", description="Add, view, and remove users")
car_tag = Tag(name="Car", description="Add, view, and remove cars")
rental_tag = Tag(name="Rental", description="Manage car rentals")


@app.get('/', tags=[home_tag])
def home():
    """Redirects the user to the OpenAPI documentation page, where they can choose the style of documentation (Swagger, Redoc, or RapiDoc)."""
    return redirect('/openapi')


@app.post('/user', tags=[user_tag], responses={"200": UserViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_user(form: UserSchema):
    """Adds a new user to the database.

    It returns the newly created user with their ID.
    """
    user = User(
        name=form.name,
        email=form.email,
        password=form.password,
        driver_license_number=form.driver_license_number
    )
    logger.debug(f"Adding user: '{user.name}'")
    try:
        session = Session()
        session.add(user)
        session.commit()
        logger.debug(f"User added: '{user.name}'")
        return present_user(user), 200
    except IntegrityError as e:
        error_msg = "User with the same email or driver license number already exists"
        logger.warning(f"Error adding user '{user.name}': {error_msg}, Exception: {str(e)}")
        return {"message": error_msg}, 409
    except Exception as e:
        error_msg = "Failed to add user"
        logger.warning(f"Error adding user '{user.name}': {error_msg}, Exception: {str(e)}")
        return {"message": error_msg}, 400


@app.get('/users', tags=[user_tag], responses={"200": UserListSchema, "404": ErrorSchema})
def get_users():
    """Retrieves all users from the database.

    This endpoint returns a list of all users stored in the database. If no users are found, an empty list is returned.
    """
    logger.debug("Retrieving all users")
    session = Session()
    users = session.query(User).all()
    if not users:
        return {"users": []}, 200
    else:
        logger.debug(f"{len(users)} users found")
        return present_users(users), 200


@app.get('/user', tags=[user_tag], responses={"200": UserViewSchema, "404": ErrorSchema})
def get_user(query: UserSearchSchema):
    """Retrieves a user from the database by their ID.

    This endpoint returns the details of a user with the specified ID. If the user is not found, it returns a 404 error.
    """
    user_id = query.id
    logger.debug(f"Retrieving user with ID: {user_id}")
    session = Session()
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        error_msg = "User not found"
        logger.warning(f"Error retrieving user with ID '{user_id}': {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"User found with ID: '{user_id}'")
        return present_user(user), 200


@app.delete('/user', tags=[user_tag], responses={"200": UserDeleteSchema, "404": ErrorSchema})
def delete_user(query: UserSearchSchema):
    """Deletes a user from the database by their ID.

    It returns a message indicating whether the deletion was successful.
    """
    user_id = query.id
    logger.debug(f"Deleting user with ID: {user_id}")

    session = Session()
    count = session.query(User).filter(User.id == user_id).delete()
    session.commit()

    if count:
        logger.debug(f"Deleted user with ID: {user_id}")
        return {"message": "User deleted successfully", "id": user_id}, 200
    else:
        error_msg = "User not found"
        logger.warning(f"Error deleting user with ID '{user_id}': {error_msg}")
        return {"message": error_msg}, 404


@app.post('/car', tags=[car_tag], responses={"200": CarViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_car(form: CarSchema):
    """Adds a new car to the database.

    It returns the newly created car with its ID and availability status.
    """
    car = Car(
        make=form.make,
        model=form.model,
        year=form.year,
        price_per_day=form.price_per_day
    )
    logger.debug(f"Adding car: '{car.make} {car.model}'")
    try:
        session = Session()
        session.add(car)
        session.commit()
        logger.debug(f"Car added: '{car.make} {car.model}'")
        return present_car(car), 200
    except IntegrityError as e:
        error_msg = "Car with the same make and model already exists"
        logger.warning(f"Error adding car '{car.make} {car.model}': {error_msg}, Exception: {str(e)}")
        return {"message": error_msg}, 409
    except Exception as e:
        error_msg = "Failed to add car"
        logger.warning(f"Error adding car '{car.make} {car.model}': {error_msg}, Exception: {str(e)}")
        return {"message": error_msg}, 400


@app.get('/cars', tags=[car_tag], responses={"200": CarListSchema, "404": ErrorSchema})
def get_cars():
    """Retrieves all cars from the database.

    It returns a list of all cars stored in the database. If no cars are found, an empty list is returned.
    """
    logger.debug("Retrieving all cars")
    session = Session()
    cars = session.query(Car).all()
    if not cars:
        return {"cars": []}, 200
    else:
        logger.debug(f"{len(cars)} cars found")
        return present_cars(cars), 200


@app.get('/car', tags=[car_tag], responses={"200": CarViewSchema, "404": ErrorSchema})
def get_car(query: CarSearchSchema):
    """Retrieves a car from the database by its ID.

    It returns the details of a car with the specified ID. If the car is not found, it returns a 404 error.
    """
    car_id = query.id
    logger.debug(f"Retrieving car with ID: {car_id}")
    session = Session()
    car = session.query(Car).filter(Car.id == car_id).first()

    if not car:
        error_msg = "Car not found"
        logger.warning(f"Error retrieving car with ID '{car_id}': {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Car found with ID: '{car_id}'")
        return present_car(car), 200


@app.delete('/car', tags=[car_tag], responses={"200": CarDeleteSchema, "404": ErrorSchema})
def delete_car(query: CarSearchSchema):
    """Deletes a car from the database by its ID.

    It returns a message indicating whether the deletion was successful.
    """
    car_id = query.id
    logger.debug(f"Deleting car with ID: {car_id}")

    session = Session()
    count = session.query(Car).filter(Car.id == car_id).delete()
    session.commit()

    if count:
        logger.debug(f"Deleted car with ID: {car_id}")
        return {"message": "Car deleted successfully", "id": car_id}, 200
    else:
        error_msg = "Car not found"
        logger.warning(f"Error deleting car with ID '{car_id}': {error_msg}")
        return {"message": error_msg}, 404


@app.post('/rental', tags=[rental_tag], responses={"200": RentalViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_rental(form: RentalSchema):
    """Adds a new rental record to the database.

    It returns the newly created rental with its ID.
    """
    logger.debug(f"Adding rental for user ID: '{form.user_id}' and car ID: '{form.car_id}'")

    session = Session()

    car = session.query(Car).filter(Car.id == form.car_id).first()
    if not car:
        error_msg = "Car not found"
        logger.warning(f"Error adding rental: {error_msg}")
        return {"message": error_msg}, 400

    price_per_day = car.price_per_day
    rental_days = (form.rental_end_date - form.rental_start_date).days
    if rental_days < 0:
        error_msg = "Invalid rental period: End date is before start date"
        logger.warning(f"Error adding rental: {error_msg}")
        return {"message": error_msg}, 400
    
    total_price = price_per_day * rental_days

    rental = Rental(
        user_id=form.user_id,
        car_id=form.car_id,
        rental_start_date=form.rental_start_date,
        rental_end_date=form.rental_end_date,
        total_price=total_price
    )

    try:
        session.add(rental)
        session.commit()
        logger.debug(f"Rental added: '{rental.id}'")
        return present_rental(rental), 200
    except IntegrityError as e:
        error_msg = "Rental with the same user and car already exists"
        logger.warning(f"Error adding rental '{rental.id}': {error_msg}, Exception: {str(e)}")
        return {"message": error_msg}, 409
    except Exception as e:
        error_msg = "Failed to add rental"
        logger.warning(f"Error adding rental '{rental.id}': {error_msg}, Exception: {str(e)}")
        return {"message": error_msg}, 400


@app.get('/rentals', tags=[rental_tag], responses={"200": RentalListSchema, "404": ErrorSchema})
def get_rentals():
    """Retrieves all rentals from the database.

    This endpoint returns a list of all rentals stored in the database. If no rentals are found, an empty list is returned.
    """
    logger.debug("Retrieving all rentals")
    session = Session()
    rentals = session.query(Rental).all()

    if not rentals:
        return {"rentals": []}, 200
    else:
        logger.debug(f"{len(rentals)} rentals found")
        return present_rentals(rentals), 200


@app.get('/rental', tags=[rental_tag], responses={"200": RentalViewSchema, "404": ErrorSchema})
def get_rental(query: RentalSearchSchema):
    """Retrieves a rental from the database by its ID.

    This endpoint returns the details of a rental with the specified ID. If the rental is not found, it returns a 404 error.
    """
    rental_id = query.id
    logger.debug(f"Retrieving rental with ID: {rental_id}")
    session = Session()
    rental = session.query(Rental).filter(Rental.id == rental_id).first()

    if not rental:
        error_msg = "Rental not found"
        logger.warning(f"Error retrieving rental with ID '{rental_id}': {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Rental found with ID: '{rental_id}'")
        return present_rental(rental), 200


@app.delete('/rental', tags=[rental_tag], responses={"200": RentalDeleteSchema, "404": ErrorSchema})
def delete_rental(query: RentalSearchSchema):
    """Deletes a rental from the database by its ID.

    It returns a message indicating whether the deletion was successful.
    """
    rental_id = query.id
    logger.debug(f"Deleting rental with ID: {rental_id}")

    session = Session()
    count = session.query(Rental).filter(Rental.id == rental_id).delete()
    session.commit()

    if count:
        logger.debug(f"Deleted rental with ID: {rental_id}")
        return {"message": "Rental deleted successfully", "id": rental_id}, 200
    else:
        error_msg = "Rental not found"
        logger.warning(f"Error deleting rental with ID '{rental_id}': {error_msg}")
        return {"message": error_msg}, 404
