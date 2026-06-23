from database import db


class Booking(db.Model):

    __tablename__ = "bookings"

    booking_id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        nullable=False
    )

    car_id = db.Column(
        db.Integer,
        nullable=False
    )

    start_date = db.Column(
        db.String(20),
        nullable=False
    )

    end_date = db.Column(
        db.String(20),
        nullable=False
    )

    status = db.Column(
        db.String(20),
        default="Pending"
    )
    total_price = db.Column(
        db.Float,
        default=0
    )

    discount = db.Column(
        db.Float,
        default=0
    )

    final_price = db.Column(
        db.Float,
        default=0
    )