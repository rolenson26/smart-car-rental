from datetime import datetime

from models import Booking, Payment


def parse_date(value):
    return datetime.strptime(value, "%Y-%m-%d").date()


def calculate_total(vehicle, booking_date, return_date):
    days = (return_date - booking_date).days + 1
    return max(days, 1) * vehicle.rental_price


def has_booking_conflict(vehicle_id, booking_date, return_date):
    active_statuses = ["Pending", "Confirmed", "Active"]
    bookings = Booking.query.filter(
        Booking.vehicle_id == vehicle_id,
        Booking.status.in_(active_statuses),
    ).all()

    for booking in bookings:
        if booking_date <= booking.return_date and return_date >= booking.booking_date:
            return True
    return False


def create_pending_payment(booking):
    return Payment(
        booking=booking,
        amount=booking.total_amount,
        payment_status="Pending",
    )
