from flask import (
    Flask,
    render_template,
    request,
    redirect,
    session,
    url_for
)
from routes.auth_routes import auth_bp

from config import Config
from database import db

from models.admin import Admin
from models.user import User
from models.owner import Owner

from routes.car_routes import car_bp
from models.car import Car
from models.booking import Booking
from routes.booking_routes import booking_bp
from routes.membership_routes import membership_bp
from models.membership import Membership



app = Flask(__name__)

app.config.from_object(Config)
app.secret_key = "smart_car_rental_secret_key"

db.init_app(app)

app.register_blueprint(
    auth_bp,
    url_prefix="/api"
)
app.register_blueprint(
    car_bp,
    url_prefix="/api"
)
app.register_blueprint(
    booking_bp,
    url_prefix="/api"
)
app.register_blueprint(
    membership_bp,
    url_prefix="/api"
)


@app.route("/")
def home():
    return render_template(
        "home.html"
    )


@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login_page():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = User.query.filter_by(
            email=email
        ).first()

        if user and user.check_password(
            password
        ):
            session["user_id"] = user.user_id
            session["user_name"] = user.full_name

            return redirect("/")

        return "Invalid email or password"

    return render_template(
        "login.html"
    )
@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.route(
    "/register",
    methods=["GET", "POST"]
)
def register_page():

    if request.method == "POST":

        user = User(
            full_name=request.form["full_name"],
            email=request.form["email"],
            phone=request.form["phone"]
        )

        user.set_password(
            request.form["password"]
        )

        db.session.add(user)
        db.session.commit()

        return redirect("/login")

    return render_template(
        "register.html"
    )
@app.route("/cars")
def cars_page():

    cars = Car.query.all()

    return render_template(
        "cars.html",
        cars=cars
    )
@app.route("/add-car")
def add_car_page():
    return render_template(
        "add_car.html"
    )

@app.route("/my-bookings")
def my_bookings_page():

    if "user_id" not in session:
        return redirect("/login")
 
    user_id = session.get("user_id")

    bookings = Booking.query.filter_by(
    user_id=user_id
    ).all()
    cars = Car.query.all()

    car_dict = {}

    for car in cars:
        car_dict[car.car_id] = (
            car.brand + " " + car.model
        )

    return render_template(
        "my_bookings.html",
        bookings=bookings,
        car_dict=car_dict
    )
@app.route("/owner-bookings")
def owner_bookings_page():

    bookings = Booking.query.all()

    return render_template(
        "owner_bookings.html",
        bookings=bookings
    )

@app.route("/api/users")
def get_users():

    users = User.query.all()

    return [
        {
            "id": user.user_id,
            "name": user.full_name,
            "email": user.email,
            "phone": user.phone
        }
        for user in users
    ]
@app.route("/check-session")
def check_session():

    return {
        "user_id": session.get("user_id"),
        "user_name": session.get("user_name")
    }
@app.route("/membership")
def membership_page():

    memberships = Membership.query.all()

    current_plan = "None"

    if "user_id" in session:

        user = User.query.get(
            session["user_id"]
        )

        current_plan = user.membership_type

    return render_template(
        "membership.html",
        memberships=memberships,
        current_plan=current_plan
    )
@app.route("/choose-membership/<int:membership_id>")
def choose_membership(membership_id):

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(
        session["user_id"]
    )

    membership = Membership.query.get(
        membership_id
    )

    user.membership_type = membership.name

    db.session.commit()

    return redirect("/membership")


with app.app_context():

    db.create_all()

    if Membership.query.count() == 0:

        basic = Membership(
            name="Basic",
            price=0,
            benefits="Standard booking access"
        )

        premium = Membership(
            name="Premium",
            price=499,
            benefits="Priority booking"
        )

        vip = Membership(
            name="VIP",
            price=999,
            benefits="Priority booking + Extra discounts"
        )

        db.session.add(basic)
        db.session.add(premium)
        db.session.add(vip)

        db.session.commit()


if __name__ == "__main__":
    app.run(
        debug=True
    )