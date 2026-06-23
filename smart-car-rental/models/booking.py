from datetime import datetime

from database import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey("vehicles.id"), nullable=False)
    booking_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), default="Pending", nullable=False)
    total_amount = db.Column(db.Float, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", back_populates="bookings")
    vehicle = db.relationship("Vehicle", back_populates="bookings")
    payment = db.relationship("Payment", back_populates="booking", uselist=False, cascade="all, delete-orphan")

    @property
    def booking_id(self):
        return self.id

    @property
    def car_id(self):
        return self.vehicle_id

    @property
    def start_date(self):
        return self.booking_date

    @property
    def end_date(self):
        return self.return_date
