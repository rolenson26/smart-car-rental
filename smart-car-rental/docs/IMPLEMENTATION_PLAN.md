# Implementation Plan

## Missing Features Report

- Completed: Unified role-based user model.
- Completed: Vehicle listing for cars, bikes, scooters, and other categories.
- Completed: Search and category filtering.
- Completed: Vehicle details page.
- Completed: Booking form, validation, conflict checking, and history.
- Completed: Payment-ready `Payment` records.
- Completed: Review model and vehicle review submission.
- Completed: Admin dashboard.
- Completed: Admin vehicle management.
- Completed: Admin user management.
- Completed: Admin booking management.
- Completed: Admin reports.
- Completed: Bootstrap 5 responsive UI.

## Architecture Improvement Report

- `app.py`: Application factory, blueprint registration, and seed data.
- `routes/`: HTTP layer only. Routes orchestrate request parsing, guards, services, and templates.
- `models/`: SQLAlchemy ORM models and relationships.
- `services/`: Business rules such as booking conflicts, totals, and search.
- `utils/`: Shared helpers such as authentication decorators.
- `templates/`: Jinja pages for user and admin workflows.
- `static/`: CSS and JavaScript assets.
- `config.py`: Runtime configuration.
- `docs/`: Audit, schema, workflow, and planning documentation.

## Priority Task List

1. Add Flask-Migrate before production deployments.
2. Add CSRF protection with Flask-WTF.
3. Add automated tests for auth, booking overlap checks, and admin guards.
4. Connect a payment gateway using the `Payment` model.
5. Add image upload storage instead of URL-only images.
6. Add pagination for large vehicle, user, and booking tables.
7. Add email notifications for booking status changes.
8. Add deployment configuration for production hosting.

## Suggested Git Commit Messages

- `refactor: introduce modular Flask app structure`
- `feat: add vehicle booking and payment-ready models`
- `feat: add admin dashboard and management pages`
- `feat: rebuild responsive Bootstrap rental UI`
- `docs: add audit schema workflow and setup documentation`
