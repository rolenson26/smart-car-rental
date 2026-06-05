from flask import Flask, render_template, request, jsonify, session
import json, os, random
from datetime import datetime

app = Flask(__name__)
app.secret_key = "carrentalsecret"

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
BOOKINGS_FILE = os.path.join(DATA_DIR, "bookings.json")
INCOME_FILE = os.path.join(DATA_DIR, "income.json")

ADMIN_PASSWORD = "1234"

CARS = [
    {"id": 1, "brand": "Toyota", "model": "Innova", "category": "SUV", "price": 2500, "available": True, "image": "/static/image/toyota.jpg"},
    {"id": 2, "brand": "Hyundai", "model": "i20", "category": "Economy", "price": 1500, "available": True, "image": "/static/image/hyundai.jpg"},
    {"id": 3, "brand": "Honda", "model": "City", "category": "Sedan", "price": 2200, "available": True, "image": "/static/image/honda.jpg"},
    {"id": 4, "brand": "BMW", "model": "X5", "category": "Luxury", "price": 5000, "available": True, "image": "/static/image/bmw.jpg"},
    {"id": 5, "brand": "Audi", "model": "A6", "category": "Luxury", "price": 5500, "available": True, "image": "/static/image/audi.jpg"},
]

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path) as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_cars():
    rented = load_json(BOOKINGS_FILE, [])
    rented_ids = {b["car_id"] for b in rented if b.get("active")}
    cars = []
    for c in CARS:
        car = dict(c)
        car["available"] = car["id"] not in rented_ids
        cars.append(car)
    return cars

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/cars")
def api_cars():
    return jsonify(get_cars())

@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    users = load_json(USERS_FILE, [])
    for u in users:
        if u["phone"] == data["phone"]:
            return jsonify({"success": False, "message": "Phone already registered!"})
    users.append({"name": data["name"], "phone": data["phone"], "license": data["license"]})
    save_json(USERS_FILE, users)
    return jsonify({"success": True, "message": "Registration successful!"})

@app.route("/api/book", methods=["POST"])
def book():
    data = request.json
    cars = get_cars()
    users = load_json(USERS_FILE, [])
    bookings = load_json(BOOKINGS_FILE, [])

    car = next((c for c in cars if c["id"] == data["car_id"] and c["available"]), None)
    if not car:
        return jsonify({"success": False, "message": "Car not available."})

    is_registered = any(u["name"].lower() == data["name"].lower() for u in users)

    base = car["price"] * data["days"]
    tax = base * 0.18
    total = base + tax
    discount = 0

    if data.get("coupon") == "SAVE10":
        discount += total * 0.10
    if is_registered:
        discount += total * 0.05

    final = round(total - discount, 2)

    booking_id = f"CR{random.randint(1000,9999)}"

    booking = {
        "booking_id": booking_id,
        "name": data["name"],
        "car_id": car["id"],
        "car_name": f"{car['brand']} {car['model']}",
        "days": data["days"],
        "base": round(base, 2),
        "tax": round(tax, 2),
        "discount": round(discount, 2),
        "total": final,
        "payment_method": data["payment_method"],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "active": True,
        "is_registered": is_registered
    }
    bookings.append(booking)
    save_json(BOOKINGS_FILE, bookings)

    income = load_json(INCOME_FILE, [])
    income.append({"amount": final, "date": booking["date"]})
    save_json(INCOME_FILE, income)

    return jsonify({"success": True, "booking": booking})

@app.route("/api/return", methods=["POST"])
def return_car():
    data = request.json
    bookings = load_json(BOOKINGS_FILE, [])
    for b in bookings:
        if b["car_id"] == data["car_id"] and b.get("active"):
            b["active"] = False
            b["late_days"] = data.get("late_days", 0)
            b["fine"] = data.get("late_days", 0) * 500
            save_json(BOOKINGS_FILE, bookings)
            return jsonify({"success": True, "fine": b["fine"]})
    return jsonify({"success": False, "message": "No active booking for this car."})

@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    if request.json.get("password") == ADMIN_PASSWORD:
        session["admin"] = True
        return jsonify({"success": True})
    return jsonify({"success": False, "message": "Wrong password!"})

@app.route("/api/admin/data")
def admin_data():
    if not session.get("admin"):
        return jsonify({"error": "Unauthorized"}), 401
    bookings = load_json(BOOKINGS_FILE, [])
    income = load_json(INCOME_FILE, [])
    users = load_json(USERS_FILE, [])
    total_income = round(sum(i["amount"] for i in income), 2)
    return jsonify({
        "bookings": bookings,
        "total_income": total_income,
        "users": users,
        "cars": get_cars()
    })

@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():
    session.pop("admin", None)
    return jsonify({"success": True})

if __name__ == "__main__":
    os.makedirs(DATA_DIR, exist_ok=True)
    app.run(debug=True)