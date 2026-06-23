from flask import Flask

from config import Config
from database import db
from models import Booking, Payment, Review, User, Vehicle
from routes.admin_routes import admin_bp
from routes.auth_routes import auth_bp
from routes.booking_routes import booking_bp
from routes.vehicle_routes import vehicle_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    app.register_blueprint(auth_bp)
    app.register_blueprint(vehicle_bp)
    app.register_blueprint(booking_bp)
    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()
        seed_database()

    return app


def seed_database():
    """Create starter data so a fresh clone opens with useful demo content."""
    if not User.query.filter_by(email="admin@smartcar.test").first():
        admin = User(
            name="Platform Admin",
            email="admin@smartcar.test",
            role="admin",
        )
        admin.set_password("admin123")
        db.session.add(admin)

    if Vehicle.query.count() == 0:
        vehicles = [
            Vehicle(
                vehicle_name="Toyota Urban Cruiser",
                category="Car",
                brand="Toyota",
                model="Urban Cruiser",
                registration_number="SCR-1001",
                rental_price=2400,
                image="https://images.unsplash.com/photo-1552519507-da3b142c6e3d?auto=format&fit=crop&w=900&q=80",
                availability_status="Available",
                seats=5,
                fuel_type="Petrol",
                transmission="Automatic",
                description="Comfortable compact SUV for city and highway trips.",
            ),
            Vehicle(
                vehicle_name="Honda Activa 6G",
                category="Scooter",
                brand="Honda",
                model="Activa 6G",
                registration_number="SCR-2001",
                rental_price=450,
                image="https://images.unsplash.com/photo-1558981806-ec527fa84c39?auto=format&fit=crop&w=900&q=80",
                availability_status="Available",
                seats=2,
                fuel_type="Petrol",
                transmission="Automatic",
                description="Easy daily scooter for short-distance rentals.",
            ),
            Vehicle(
                vehicle_name="Royal Enfield Classic",
                category="Bike",
                brand="Royal Enfield",
                model="Classic 350",
                registration_number="SCR-3001",
                rental_price=1200,
                image="https://images.unsplash.com/photo-1558981359-219d6364c9c8?auto=format&fit=crop&w=900&q=80",
                availability_status="Available",
                seats=2,
                fuel_type="Petrol",
                transmission="Manual",
                description="Touring-ready bike for weekend escapes.",
            ),
        ]
        db.session.add_all(vehicles)

    db.session.commit()


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)
