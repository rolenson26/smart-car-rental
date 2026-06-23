from database import db
from datetime import datetime


class Car(db.Model):

    __tablename__ = "cars"

    car_id = db.Column(
        db.Integer,
        primary_key=True
    )

    owner_id = db.Column(
        db.Integer,
        nullable=False
    )

    brand = db.Column(
        db.String(100),
        nullable=False
    )

    model = db.Column(
        db.String(100),
        nullable=False
    )

    year = db.Column(
        db.Integer,
        nullable=False
    )

    fuel_type = db.Column(
        db.String(50),
        nullable=False
    )

    transmission = db.Column(
        db.String(50),
        nullable=False
    )

    seats = db.Column(
        db.Integer,
        nullable=False
    )

    price_per_day = db.Column(
        db.Float,
        nullable=False
    )

    image = db.Column(
        db.String(255)
    )

    rating = db.Column(
        db.Float,
        default=0
    )

    availability = db.Column(
        db.Boolean,
        default=True
    )

    description = db.Column(
        db.Text
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )