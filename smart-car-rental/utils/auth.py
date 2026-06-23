from functools import wraps

from flask import flash, redirect, session, url_for

from models import User


def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return None
    return User.query.get(user_id)


def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if not current_user():
            flash("Please log in to continue.", "warning")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped_view


def admin_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        user = current_user()
        if not user or user.role != "admin":
            flash("Admin access is required for that page.", "danger")
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped_view
