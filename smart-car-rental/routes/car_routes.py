from flask import Blueprint
from flask import request
from flask import jsonify

from database import db
from models.car import Car

car_bp = Blueprint(
    "cars",
    __name__
)


@car_bp.route(
    "/cars",
    methods=["GET"]
)
def get_cars():

    cars = Car.query.all()

    result = []

    for car in cars:

        result.append({
            "car_id": car.car_id,
            "brand": car.brand,
            "model": car.model,
            "price": car.price_per_day,
            "rating": car.rating
        })

    return jsonify(result)


@car_bp.route(
    "/cars/add",
    methods=["POST"]
)
def add_car():

    data = request.get_json()

    car = Car(
        owner_id=data["owner_id"],
        brand=data["brand"],
        model=data["model"],
        year=data["year"],
        fuel_type=data["fuel_type"],
        transmission=data["transmission"],
        seats=data["seats"],
        price_per_day=data["price_per_day"],
        description=data["description"]
    )

    db.session.add(car)
    db.session.commit()

    return jsonify({
        "message": "Car added successfully"
    })