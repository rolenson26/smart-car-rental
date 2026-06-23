# Development Workflow

## How a User Books a Vehicle

1. User registers or logs in.
2. User opens `/vehicles` and searches by brand, model, category, or registration number.
3. User opens the vehicle details page.
4. User selects booking and return dates.
5. The backend validates dates and checks overlapping active bookings.
6. The backend creates a `Booking` and a pending `Payment`.
7. User sees the booking in `/my-bookings`.

```mermaid
flowchart TD
    A[Browse vehicles] --> B[Open vehicle details]
    B --> C[Submit booking dates]
    C --> D{Logged in?}
    D -- No --> E[Redirect to login]
    D -- Yes --> F[Validate dates]
    F --> G{Vehicle available?}
    G -- No --> H[Show error]
    G -- Yes --> I[Create booking]
    I --> J[Create pending payment]
    J --> K[Show booking history]
```

## How an Admin Adds Vehicles

1. Admin logs in with an admin account.
2. Admin opens `/admin/vehicles`.
3. Admin clicks Add vehicle.
4. Admin submits vehicle data.
5. The route validates required form fields.
6. SQLAlchemy inserts the vehicle row.
7. Vehicle appears in public listings.

```mermaid
flowchart TD
    A[Admin dashboard] --> B[Vehicle management]
    B --> C[Add vehicle form]
    C --> D[Validate form]
    D --> E[Insert Vehicle]
    E --> F[Public vehicle listing]
```

## Booking Data Flow

```mermaid
flowchart LR
    Form[Booking Form] --> Route[booking.book_vehicle]
    Route --> Service[booking_service]
    Service --> DB[(SQLite)]
    DB --> Booking[Booking Row]
    DB --> Payment[Pending Payment Row]
```

## Request Lifecycle

1. Browser sends request to Flask route.
2. Blueprint route handles authentication guard if required.
3. Route reads form data or JSON.
4. Service functions perform business checks.
5. SQLAlchemy ORM reads or writes database rows.
6. Route flashes a message or returns JSON.
7. Template renders the response.

## Database Interactions

- Reads use SQLAlchemy query APIs, for example `Vehicle.query.get_or_404`.
- Writes use `db.session.add`, `db.session.flush` when related IDs are needed, and `db.session.commit`.
- Booking creation writes both `bookings` and `payments`.
- Admin status updates modify existing booking rows.
