from flask import Blueprint, request, jsonify, session
from database import db
from models.booking import Booking
from datetime import datetime

booking_bp = Blueprint(
    "booking_bp",
    __name__
)
@booking_bp.route(
    "/bookings/add",
    methods=["POST"]
)
@booking_bp.route(
    "/bookings/add",
    methods=["POST"]
)
def add_booking():

    data = request.json

    start_date = datetime.strptime(
        data["start_date"],
        "%Y-%m-%d"
    )

    end_date = datetime.strptime(
        data["end_date"],
        "%Y-%m-%d"
    )

    if end_date < start_date:
        return jsonify({
            "message":
            "End date must be after start date"
        }), 400

    existing_bookings = Booking.query.filter_by(
        car_id=data["car_id"]
    ).all()

    for b in existing_bookings:

        existing_start = datetime.strptime(
            str(b.start_date),
            "%Y-%m-%d"
        )

        existing_end = datetime.strptime(
            str(b.end_date),
            "%Y-%m-%d"
        )

        if (
            start_date <= existing_end and
            end_date >= existing_start
        ):
            return jsonify({
                "message":
                "Car already booked for these dates"
            }), 400

    if "user_id" not in session:
        return jsonify({
            "message":
            "Please login first"
        }), 401

    booking = Booking(
        user_id=session["user_id"],
        car_id=data["car_id"],
        start_date=data["start_date"],
        end_date=data["end_date"]
    )

    db.session.add(booking)
    db.session.commit()

    return jsonify({
        "message":
        "Booking created successfully"
    })
@booking_bp.route(
    "/bookings/delete/<int:booking_id>",
    methods=["DELETE"]
)
def delete_booking(booking_id):

    booking = Booking.query.get(
        booking_id
    )

    if booking:

        db.session.delete(
            booking
        )

        db.session.commit()

        return jsonify({
            "message":
            "Booking cancelled"
        })
@booking_bp.route(
    "/bookings/update-status/<int:booking_id>",
    methods=["PUT"]
)
def update_booking_status(booking_id):

    booking = Booking.query.get(
        booking_id
    )

    if not booking:
        return jsonify({
            "message":
            "Booking not found"
        }), 404

    data = request.json

    booking.status = data["status"]

    db.session.commit()

    return jsonify({
        "message":
        "Status updated"
    })    
@booking_bp.route(
    "/bookings"
)
def get_bookings():

    bookings = Booking.query.all()

    result = []

    for booking in bookings:

        result.append({
            "booking_id": booking.booking_id,
            "user_id": booking.user_id,
            "car_id": booking.car_id,
            "start_date": booking.start_date,
            "end_date": booking.end_date,
            "status": booking.status
        })

    return jsonify(result)


    return jsonify({
        "message":
        "Booking not found"
    })