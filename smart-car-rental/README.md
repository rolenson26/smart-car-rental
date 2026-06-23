# Smart Car Rental

## Project Overview

Smart Car Rental is a Flask and SQLAlchemy vehicle rental platform for cars, bikes, scooters, and other vehicles. Users can register, search vehicles, book rentals, track booking history, and add reviews. Admins can manage vehicles, users, bookings, and view operational reports.

## Features

- User registration and login
- Vehicle listing, search, filtering, and details
- Vehicle booking with date validation and conflict checks
- Booking history and cancellation
- Admin dashboard
- Vehicle CRUD management
- User role management
- Booking status tracking
- Payment-ready architecture with pending payment rows
- Review and rating support
- Responsive Bootstrap 5 frontend

## Technology Stack

Frontend:

- HTML
- CSS
- Bootstrap 5
- JavaScript

Backend:

- Flask
- SQLAlchemy
- Flask-SQLAlchemy

Database:

- SQLite

## Installation

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

On Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

Default seeded admin:

- Email: `admin@smartcar.test`
- Password: `admin123`

## Project Structure

- `app.py`: Flask application factory, blueprint registration, and seed data.
- `config.py`: App settings, secret key, and database URL.
- `database.py`: Shared SQLAlchemy database instance.
- `models/`: ORM models for users, vehicles, bookings, payments, and reviews.
- `routes/`: Flask blueprints for auth, vehicles, bookings, and admin pages/APIs.
- `services/`: Business logic for booking calculations, overlap checks, and vehicle search.
- `utils/`: Shared route guards and current-user helper.
- `templates/`: Jinja templates for public, user, and admin pages.
- `static/`: CSS and JavaScript assets.
- `docs/`: Audit, database design, workflow, and implementation planning documents.
- `instance/`: Local SQLite database files.

## Database Schema

Core tables:

- `users`: Account identity, password hash, role, and profile data.
- `vehicles`: Rental inventory across cars, bikes, scooters, and other categories.
- `bookings`: User rental requests with dates, status, and total amount.
- `payments`: Payment-ready records linked one-to-one with bookings.
- `reviews`: User ratings and comments for vehicles.

Full details are in `docs/DATABASE_DESIGN.md`.

## API Routes

- `POST /api/register`: Create a user account.
- `POST /api/login`: Log in and create a session.
- `GET /api/users`: List users.
- `GET /api/vehicles`: List/search vehicles.
- `GET /api/cars`: Compatibility alias for vehicles.
- `GET /api/bookings`: List bookings.
- `POST /api/bookings/add`: Create a booking.
- `DELETE /api/bookings/delete/<booking_id>`: Cancel a booking.
- `PUT /api/bookings/update-status/<booking_id>`: Update booking status as admin.

## Screenshots Section

Add screenshots here after running the app locally:

- Home page
- Vehicle listing
- Vehicle details
- Booking history
- Admin dashboard
- Vehicle management

## Dependency Audit

- `Flask`: Web framework, routing, sessions, templates, and request handling.
- `Flask-SQLAlchemy`: Flask integration for SQLAlchemy.
- `SQLAlchemy`: ORM and database query layer.
- `Werkzeug`: Password hashing and Flask utility dependency.

## Future Improvements

- Add Flask-Migrate for production schema migrations.
- Add CSRF protection with Flask-WTF.
- Add automated tests.
- Connect a real payment provider.
- Add image uploads.
- Add pagination and sorting for admin tables.
- Add email or SMS booking notifications.
- Add production deployment configuration.
