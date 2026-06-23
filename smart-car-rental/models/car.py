from datetime import datetime

from database import db


class Vehicle(db.Model):
    __tablename__ = "vehicles"

    id = db.Column(db.Integer, primary_key=True)
    vehicle_name = db.Column(db.String(120), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    brand = db.Column(db.String(80), nullable=False)
    model = db.Column(db.String(80), nullable=False)
    registration_number = db.Column(db.String(40), unique=True, nullable=False)
    rental_price = db.Column(db.Float, nullable=False)
    image = db.Column(db.String(500))
    availability_status = db.Column(db.String(30), default="Available", nullable=False)
    seats = db.Column(db.Integer, default=4)
    fuel_type = db.Column(db.String(40), default="Petrol")
    transmission = db.Column(db.String(40), default="Manual")
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    bookings = db.relationship("Booking", back_populates="vehicle", cascade="all, delete-orphan")
    reviews = db.relationship("Review", back_populates="vehicle", cascade="all, delete-orphan")

    @property
    def car_id(self):
        return self.id

    @property
    def price_per_day(self):
        return self.rental_price

    @price_per_day.setter
    def price_per_day(self, value):
        self.rental_price = value

    @property
    def availability(self):
        return self.availability_status == "Available"

    @property
    def average_rating(self):
        if not self.reviews:
            return 0
        return round(sum(review.rating for review in self.reviews) / len(self.reviews), 1)


Car = Vehicle
