from flask import Blueprint, flash, redirect, render_template, request, url_for

from database import db
from models import Booking, Payment, User, Vehicle
from utils.auth import admin_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@admin_required
def dashboard():
    stats = {
        "vehicles": Vehicle.query.count(),
        "users": User.query.count(),
        "bookings": Booking.query.count(),
        "revenue": db.session.query(db.func.coalesce(db.func.sum(Payment.amount), 0)).filter(Payment.payment_status == "Paid").scalar(),
    }
    recent_bookings = Booking.query.order_by(Booking.created_at.desc()).limit(6).all()
    return render_template("admin/dashboard.html", stats=stats, recent_bookings=recent_bookings)


@admin_bp.route("/vehicles")
@admin_required
def vehicles():
    return render_template("admin/vehicles.html", vehicles=Vehicle.query.order_by(Vehicle.created_at.desc()).all())


@admin_bp.route("/vehicles/new", methods=["GET", "POST"])
@admin_required
def new_vehicle():
    if request.method == "POST":
        vehicle = Vehicle()
        update_vehicle_from_form(vehicle)
        db.session.add(vehicle)
        db.session.commit()
        flash("Vehicle added.", "success")
        return redirect(url_for("admin.vehicles"))
    return render_template("admin/vehicle_form.html", vehicle=None)


@admin_bp.route("/vehicles/<int:vehicle_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    if request.method == "POST":
        update_vehicle_from_form(vehicle)
        db.session.commit()
        flash("Vehicle updated.", "success")
        return redirect(url_for("admin.vehicles"))
    return render_template("admin/vehicle_form.html", vehicle=vehicle)


@admin_bp.route("/vehicles/<int:vehicle_id>/delete", methods=["POST"])
@admin_required
def delete_vehicle(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)
    db.session.delete(vehicle)
    db.session.commit()
    flash("Vehicle removed.", "info")
    return redirect(url_for("admin.vehicles"))


@admin_bp.route("/users")
@admin_required
def users():
    return render_template("admin/users.html", users=User.query.order_by(User.created_at.desc()).all())


@admin_bp.route("/users/<int:user_id>/role", methods=["POST"])
@admin_required
def update_user_role(user_id):
    user = User.query.get_or_404(user_id)
    role = request.form.get("role")
    if role in ["user", "admin"]:
        user.role = role
        db.session.commit()
        flash("User role updated.", "success")
    return redirect(url_for("admin.users"))


@admin_bp.route("/bookings")
@admin_required
def bookings():
    return render_template("admin/bookings.html", bookings=Booking.query.order_by(Booking.created_at.desc()).all())


@admin_bp.route("/bookings/<int:booking_id>/status", methods=["POST"])
@admin_required
def update_booking_status(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    status = request.form.get("status")
    if status in ["Pending", "Confirmed", "Active", "Completed", "Cancelled"]:
        booking.status = status
        db.session.commit()
        flash("Booking status updated.", "success")
    return redirect(url_for("admin.bookings"))


@admin_bp.route("/reports")
@admin_required
def reports():
    bookings_by_status = db.session.query(Booking.status, db.func.count(Booking.id)).group_by(Booking.status).all()
    vehicles_by_category = db.session.query(Vehicle.category, db.func.count(Vehicle.id)).group_by(Vehicle.category).all()
    return render_template("admin/reports.html", bookings_by_status=bookings_by_status, vehicles_by_category=vehicles_by_category)


def update_vehicle_from_form(vehicle):
    vehicle.vehicle_name = request.form["vehicle_name"].strip()
    vehicle.category = request.form["category"].strip()
    vehicle.brand = request.form["brand"].strip()
    vehicle.model = request.form["model"].strip()
    vehicle.registration_number = request.form["registration_number"].strip().upper()
    vehicle.rental_price = float(request.form["rental_price"])
    vehicle.image = request.form.get("image", "").strip()
    vehicle.availability_status = request.form.get("availability_status", "Available")
    vehicle.seats = int(request.form.get("seats") or 4)
    vehicle.fuel_type = request.form.get("fuel_type", "Petrol")
    vehicle.transmission = request.form.get("transmission", "Manual")
    vehicle.description = request.form.get("description", "").strip()
