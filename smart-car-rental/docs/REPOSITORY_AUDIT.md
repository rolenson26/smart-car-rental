# Repository Audit Report

## Existing Structure

- `app.py`: Previously mixed app setup, page routes, API routes, seed logic, and session handling in one file. It is now a Flask application factory and seed entrypoint.
- `config.py`: Holds application configuration, secret key, and SQLite database URI.
- `database.py`: Owns the shared SQLAlchemy `db` instance.
- `models/`: Database models. The original project had `User`, `Car`, `Booking`, `Membership`, `Admin`, and `Owner`; several lacked relationships. The reconstructed model layer now centers on `User`, `Vehicle`, `Booking`, `Payment`, and `Review`.
- `routes/`: Flask blueprints. Original route modules mixed JSON APIs with page behavior and had duplicate booking routes. Reconstructed routes separate auth, vehicles, bookings, and admin operations.
- `services/`: Added business logic for booking date parsing, overlap checks, totals, payment creation, and vehicle search.
- `utils/`: Added authentication helpers and route guards.
- `templates/`: Original templates existed for home, auth, cars, bookings, add-car, owner bookings, and membership. Many pages were incomplete or alert-driven. Rebuilt templates now cover user and admin workflows.
- `static/`: Original CSS was basic and JavaScript was empty. Rebuilt CSS supports Bootstrap 5 layouts; JavaScript adds booking date constraints.
- `instance/`: Contains local SQLite database files and should not be treated as source code.

## Existing Features Found

- User registration and login forms.
- Session-backed login state.
- Car listing page.
- Add-car API and page prototype.
- Booking creation API with date conflict checks.
- My bookings page.
- Owner booking approval prototype.
- Membership model and page prototype.

## Broken or Incomplete Areas Found

- Duplicate `/api/bookings/add` decorators.
- Booking delete route had unreachable fallback code.
- Most models had no foreign keys or relationships.
- `review.py`, `admin_routes.py`, and `owner_routes.py` were empty.
- Navigation linked to placeholder pages.
- Templates contained mojibake characters from encoding issues.
- `book.html` relied on alert debugging and did not redirect after success.
- `/book/<id>` was linked by templates but not defined in `app.py`.
- Admin dashboard, user management, reports, vehicle edit/delete, and payment models were missing.
- Old `Car` model only supported cars, while the product requirement includes bikes, scooters, and other vehicles.

## Dead or Unused Files

- Python `__pycache__/` folders are generated runtime artifacts.
- `templates/index.html` is a database smoke-test page and is not part of the active navigation.
- `models/admin.py`, `models/owner.py`, and membership files are legacy-specific and not part of the new unified role-based architecture.

## Current Route Map

- `/`: Home page.
- `/register`, `/login`, `/logout`, `/profile`: Authentication and profile pages.
- `/vehicles`, `/cars`: Vehicle listing and search.
- `/vehicles/<vehicle_id>`: Vehicle details and reviews.
- `/vehicles/<vehicle_id>/book`, `/book/<vehicle_id>`: Booking form.
- `/my-bookings`: User booking history.
- `/admin/`: Admin dashboard.
- `/admin/vehicles`: Vehicle management.
- `/admin/vehicles/new`: Add vehicle.
- `/admin/vehicles/<vehicle_id>/edit`: Edit vehicle.
- `/admin/users`: User management.
- `/admin/bookings`: Booking management.
- `/admin/reports`: Reporting.
- `/api/register`, `/api/login`, `/api/users`: Auth/user JSON endpoints.
- `/api/vehicles`, `/api/cars`: Vehicle JSON endpoints.
- `/api/bookings`: Booking JSON endpoint.
- `/api/bookings/add`: Create booking JSON endpoint.
- `/api/bookings/delete/<booking_id>`: Cancel booking JSON endpoint.
- `/api/bookings/update-status/<booking_id>`: Admin booking status JSON endpoint.
