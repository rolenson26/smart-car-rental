from sqlalchemy import or_

from models import Vehicle


def search_vehicles(query=None, category=None, status=None):
    vehicles = Vehicle.query

    if query:
        like_query = f"%{query.strip()}%"
        vehicles = vehicles.filter(
            or_(
                Vehicle.vehicle_name.ilike(like_query),
                Vehicle.brand.ilike(like_query),
                Vehicle.model.ilike(like_query),
                Vehicle.registration_number.ilike(like_query),
            )
        )

    if category:
        vehicles = vehicles.filter(Vehicle.category == category)

    if status:
        vehicles = vehicles.filter(Vehicle.availability_status == status)

    return vehicles.order_by(Vehicle.created_at.desc()).all()
