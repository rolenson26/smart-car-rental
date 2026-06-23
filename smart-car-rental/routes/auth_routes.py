from flask import Blueprint
from flask import request
from flask import jsonify

from database import db
from models.user import User

auth_bp = Blueprint(
    "auth",
    __name__
)


@auth_bp.route(
    "/register",
    methods=["POST"]
)
def register():

    data = request.get_json()

    full_name = data.get("full_name")
    email = data.get("email")
    phone = data.get("phone")
    password = data.get("password")

    existing_email = User.query.filter_by(
        email=email
    ).first()

    if existing_email:
        return jsonify({
            "message": "Email already exists"
        }), 400

    existing_phone = User.query.filter_by(
        phone=phone
    ).first()

    if existing_phone:
        return jsonify({
            "message": "Phone already exists"
        }), 400

    user = User(
        full_name=full_name,
        email=email,
        phone=phone
    )

    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return jsonify({
        "message": "Registration successful"
    }), 201


@auth_bp.route(
    "/login",
    methods=["POST"]
)
def login():

    data = request.get_json()

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter(
        (User.email == username) |
        (User.phone == username)
    ).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    if not user.check_password(password):
        return jsonify({
            "message": "Invalid password"
        }), 401

    return jsonify({
        "message": "Login successful",
        "user_id": user.user_id,
        "name": user.full_name
    }), 200