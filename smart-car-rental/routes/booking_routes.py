from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from database import db
from models import Booking, Vehicle
from services.booking_service import calculate_total, create_pending_payment, has_booking_conflict, parse_date
from utils.auth import current_user, login_required

booking_bp = Blueprint("booking", __name__)


@booking_bp.route("/vehicles/<int:vehicle_id>/book", methods=["GET", "POST"])
@login_required
def book_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    if request.method == "POST":
        try:
            booking_date = parse_date(request.form.get("booking_date", ""))
            return_date = parse_date(request.form.get("return_date", ""))
        except ValueError:
            flash("Please select valid booking and return dates.", "danger")
            return render_template("book.html", vehicle=vehicle)

        if return_date < booking_date:
            flash("Return date must be on or after the booking date.", "danger")
            return render_template("book.html", vehicle=vehicle)

        if vehicle.availability_status != "Available" or has_booking_conflict(vehicle.id, booking_date, return_date):
            flash("This vehicle is not available for the selected dates.", "danger")
            return render_template("book.html", vehicle=vehicle)

        booking = Booking(
            user=current_user(),
            vehicle=vehicle,
            booking_date=booking_date,
            return_date=return_date,
            status="Pending",
            total_amount=calculate_total(vehicle, booking_date, return_date),
        )
        db.session.add(booking)
        db.session.flush()
        db.session.add(create_pending_payment(booking))
        db.session.commit()
        flash("Booking request created. Payment is ready to be connected.", "success")
        return redirect(url_for("booking.my_bookings"))

    return render_template("book.html", vehicle=vehicle)


@booking_bp.route("/my-bookings")
@login_required
def my_bookings():
    bookings = Booking.query.filter_by(user_id=current_user().id).order_by(Booking.created_at.desc()).all()
    return render_template("my_bookings.html", bookings=bookings)


@booking_bp.route("/owner-bookings")
@login_required
def legacy_owner_bookings():
    if current_user().role != "admin":
        flash("Admin access is required for that page.", "danger")
        return redirect(url_for("vehicle.list_vehicles"))
    return redirect(url_for("admin.bookings"))


@booking_bp.route("/bookings/<int:booking_id>/cancel", methods=["POST"])
@login_required
def cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    if booking.user_id != current_user().id and current_user().role != "admin":
        flash("You can only cancel your own bookings.", "danger")
        return redirect(url_for("booking.my_bookings"))

    booking.status = "Cancelled"
    db.session.commit()
    flash("Booking cancelled.", "info")
    return redirect(url_for("booking.my_bookings"))


@booking_bp.route("/api/bookings", methods=["GET"])
def api_bookings():
    bookings = Booking.query.order_by(Booking.created_at.desc()).all()
    return jsonify([serialize_booking(booking) for booking in bookings])


@booking_bp.route("/api/bookings/add", methods=["POST"])
@login_required
def api_add_booking():
    data = request.get_json() or {}
    vehicle = Vehicle.query.get_or_404(data.get("vehicle_id") or data.get("car_id"))
    booking_date = parse_date(data.get("booking_date") or data.get("start_date"))
    return_date = parse_date(data.get("return_date") or data.get("end_date"))

    if return_date < booking_date:
        return jsonify({"message": "Return date must be on or after booking date"}), 400

    if has_booking_conflict(vehicle.id, booking_date, return_date):
        return jsonify({"message": "Vehicle already booked for these dates"}), 400

    booking = Booking(
        user=current_user(),
        vehicle=vehicle,
        booking_date=booking_date,
        return_date=return_date,
        total_amount=calculate_total(vehicle, booking_date, return_date),
    )
    db.session.add(booking)
    db.session.flush()
    db.session.add(create_pending_payment(booking))
    db.session.commit()
    return jsonify({"message": "Booking created successfully", "booking": serialize_booking(booking)}), 201


@booking_bp.route("/api/bookings/delete/<int:booking_id>", methods=["DELETE"])
@login_required
def api_cancel_booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    booking.status = "Cancelled"
    db.session.commit()
    return jsonify({"message": "Booking cancelled"})


@booking_bp.route("/api/bookings/update-status/<int:booking_id>", methods=["PUT"])
@login_required
def api_update_booking_status(booking_id):
    if current_user().role != "admin":
        return jsonify({"message": "Admin access required"}), 403

    booking = Booking.query.get_or_404(booking_id)
    status = (request.get_json() or {}).get("status")
    if status not in ["Pending", "Confirmed", "Active", "Completed", "Cancelled"]:
        return jsonify({"message": "Invalid status"}), 400

    booking.status = status
    db.session.commit()
    return jsonify({"message": "Status updated", "booking": serialize_booking(booking)})


def serialize_booking(booking):
    return {
        "id": booking.id,
        "user_id": booking.user_id,
        "vehicle_id": booking.vehicle_id,
        "booking_date": booking.booking_date.isoformat(),
        "return_date": booking.return_date.isoformat(),
        "status": booking.status,
        "total_amount": booking.total_amount,
        "payment_status": booking.payment.payment_status if booking.payment else None,
    }
