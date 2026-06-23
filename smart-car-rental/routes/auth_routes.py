from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

from database import db
from models import User
from utils.auth import current_user, login_required

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/")
def home():
    return render_template("home.html")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        phone = request.form.get("phone", "").strip()

        if not name or not email or not password:
            flash("Name, email, and password are required.", "danger")
            return render_template("register.html")

        if User.query.filter_by(email=email).first():
            flash("An account already exists with that email.", "danger")
            return render_template("register.html")

        user = User(name=name, email=email, phone=phone, role="user")
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash("Registration successful. Please log in.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return render_template("login.html")

        session["user_id"] = user.id
        session["user_name"] = user.name
        session["user_role"] = user.role
        flash(f"Welcome back, {user.name}.", "success")
        return redirect(url_for("admin.dashboard" if user.role == "admin" else "vehicle.list_vehicles"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user())


@auth_bp.route("/api/register", methods=["POST"])
def api_register():
    data = request.get_json() or {}
    name = data.get("name") or data.get("full_name")
    email = (data.get("email") or "").lower()
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "name, email, and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(name=name, email=email, phone=data.get("phone"), role=data.get("role", "user"))
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Registration successful", "user_id": user.id}), 201


@auth_bp.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    user = User.query.filter_by(email=(data.get("email") or data.get("username") or "").lower()).first()

    if not user or not user.check_password(data.get("password", "")):
        return jsonify({"message": "Invalid credentials"}), 401

    session["user_id"] = user.id
    session["user_name"] = user.name
    session["user_role"] = user.role
    return jsonify({"message": "Login successful", "user_id": user.id, "role": user.role})


@auth_bp.route("/api/users")
def api_users():
    users = User.query.order_by(User.created_at.desc()).all()
    return jsonify([
        {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role,
            "created_at": user.created_at.isoformat(),
        }
        for user in users
    ])
