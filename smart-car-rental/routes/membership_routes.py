from flask import Blueprint, jsonify
from models.membership import Membership

membership_bp = Blueprint(
    "membership_bp",
    __name__
)


@membership_bp.route("/memberships")
def get_memberships():

    memberships = Membership.query.all()

    return jsonify([
        {
            "id": m.membership_id,
            "name": m.name,
            "price": m.price,
            "benefits": m.benefits
        }
        for m in memberships
    ])