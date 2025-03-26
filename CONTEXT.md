# Alumni Portal Project Context

## Project Structure

```
Alumni-portal-scratch/
├── app/
│   ├── routes/
│   │   ├── admin.py    # Admin-specific routes
│   │   ├── user.py     # User-specific routes
│   │   └── __init__.py
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   │   ├── admin/      # Admin-related templates
│   │   ├── base.html   # Base template
│   │   └── login.html  # Login page
│   ├── models.py       # Database models
│   └── __init__.py     # App initialization
├── config.py           # Configuration settings
├── run.py             # Application entry point
└── requirements.txt   # Project dependencies
```

## Key Components

### Models

-   **Admin**: Administrative user management
-   **User**: Alumni user management
-   **Event**: Event management and tracking
-   **user_event**: Association table for users and events

### Routes

-   **/login**: User authentication
-   **/add_users**: Bulk user addition (admin)

### Database

-   SQLite database with SQLAlchemy ORM
-   Supports user authentication and event tracking
-   Includes user-event relationships

### Security

-   Password hashing using Bcrypt
-   Session management
-   Environment variable configuration

## Development Setup

1. Create virtual environment
2. Install dependencies: `pip install -r requirements.txt`
3. Set environment variables in `.flaskenv`
4. Initialize database: `flask db upgrade`
5. Run application: `flask run`

## Authentication Flow

1. Users login with register number and password
2. Admin authentication through separate interface
3. Passwords are hashed using Bcrypt

## Features

-   User authentication
-   Event management
-   Alumni tracking
-   Admin dashboard
-   Bulk user import
