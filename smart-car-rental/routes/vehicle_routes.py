from flask import Blueprint, flash, jsonify, redirect, render_template, request, url_for

from database import db
from models import Review, Vehicle
from services.vehicle_service import search_vehicles
from utils.auth import admin_required, current_user, login_required

vehicle_bp = Blueprint("vehicle", __name__)


@vehicle_bp.route("/vehicles")
@vehicle_bp.route("/cars")
def list_vehicles():
    query = request.args.get("q")
    category = request.args.get("category")
    vehicles = search_vehicles(query=query, category=category, status=request.args.get("status"))
    categories = [row[0] for row in db.session.query(Vehicle.category).distinct().order_by(Vehicle.category)]
    return render_template("vehicles.html", vehicles=vehicles, categories=categories, query=query, selected_category=category)


@vehicle_bp.route("/vehicles/<int:vehicle_id>", methods=["GET", "POST"])
def vehicle_details(vehicle_id):
    vehicle = Vehicle.query.get_or_404(vehicle_id)

    if request.method == "POST":
        user = current_user()
        if not user:
            flash("Please log in to add a review.", "warning")
            return redirect(url_for("auth.login"))

        rating = int(request.form.get("rating", 0))
        comment = request.form.get("comment", "").strip()
        if rating < 1 or rating > 5:
            flash("Rating must be between 1 and 5.", "danger")
        else:
            db.session.add(Review(user=user, vehicle=vehicle, rating=rating, comment=comment))
            db.session.commit()
            flash("Review added.", "success")
        return redirect(url_for("vehicle.vehicle_details", vehicle_id=vehicle.id))

    return render_template("vehicle_details.html", vehicle=vehicle)


@vehicle_bp.route("/book/<int:vehicle_id>")
@login_required
def legacy_book(vehicle_id):
    return redirect(url_for("booking.book_vehicle", vehicle_id=vehicle_id))


@vehicle_bp.route("/add-car")
@admin_required
def legacy_add_car():
    return redirect(url_for("admin.new_vehicle"))


@vehicle_bp.route("/api/cars")
@vehicle_bp.route("/api/vehicles")
def api_vehicles():
    vehicles = search_vehicles(
        query=request.args.get("q"),
        category=request.args.get("category"),
        status=request.args.get("status"),
    )
    return jsonify([
        {
            "id": vehicle.id,
            "vehicle_name": vehicle.vehicle_name,
            "category": vehicle.category,
            "brand": vehicle.brand,
            "model": vehicle.model,
            "registration_number": vehicle.registration_number,
            "rental_price": vehicle.rental_price,
            "availability_status": vehicle.availability_status,
            "rating": vehicle.average_rating,
        }
        for vehicle in vehicles
    ])
