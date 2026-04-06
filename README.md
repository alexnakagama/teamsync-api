# TeamSync API

A RESTful API for team task management built with FastAPI and PostgreSQL. It provides user authentication with JWT tokens, role-based access control, and full task lifecycle management.

---

## Table of Contents

- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Data Models](#data-models)
- [API Reference](#api-reference)
- [Authentication](#authentication)
- [Role-Based Access Control](#role-based-access-control)
- [Getting Started](#getting-started)
- [Environment Variables](#environment-variables)
- [Database Migrations](#database-migrations)
- [Running the Application](#running-the-application)

---

## Tech Stack

| Layer            | Technology                        |
|------------------|-----------------------------------|
| Framework        | FastAPI 0.135+                    |
| Language         | Python 3.12+                      |
| Database         | PostgreSQL 16                     |
| ORM              | SQLAlchemy 2.0                    |
| Migrations       | Alembic 1.18+                     |
| Validation       | Pydantic v2                       |
| Authentication   | JWT (PyJWT)                       |
| Password Hashing | Passlib with Argon2               |
| Server           | Uvicorn                           |
| Containerization | Docker / Docker Compose           |

---

## Architecture

The application follows a layered architecture with a clear separation of concerns:

```
HTTP Request
    |
    v
Router  (app/api/routers/)       - Route definition and HTTP method binding
    |
    v
Dependency  (app/api/deps.py)    - Authentication, DB session injection
    |
    v
Service  (app/services/)         - Business logic
    |
    v
Model  (app/models/)             - SQLAlchemy ORM models
    |
    v
Database  (PostgreSQL)
```

Schemas (app/schemas/) are used for input validation (Pydantic) and response serialization at the router and service layers.

---

## Project Structure

```
teamsync-api/
├── alembic/                    # Database migration scripts
│   ├── env.py
│   └── versions/
├── app/
│   ├── main.py                 # Application entry point
│   ├── api/
│   │   ├── deps.py             # Shared dependencies (auth, DB session)
│   │   └── routers/
│   │       ├── users_router.py # User and task read endpoints
│   │       └── manager_router.py # Manager-only endpoints
│   ├── core/
│   │   ├── config.py           # Settings loaded from .env
│   │   └── security.py         # Password hashing, JWT creation and validation
│   ├── db/
│   │   └── database.py         # SQLAlchemy engine and session factory
│   ├── models/
│   │   ├── user.py             # User ORM model
│   │   └── task.py             # Task ORM model
│   ├── schemas/
│   │   ├── user/               # UserRegister, UserOut, UserLogin
│   │   └── task/               # TaskCreate, TaskOut
│   └── services/
│       ├── user_service.py     # Registration, login, account info
│       └── task_service.py     # Task CRUD logic
├── docker-compose.yml
├── alembic.ini
└── pyproject.toml
```

---

## Data Models

### User

| Column      | Type    | Constraints              |
|-------------|---------|--------------------------|
| id          | Integer | Primary key, indexed     |
| username    | String  | Unique, indexed          |
| email       | String  | Unique, indexed          |
| role        | String  | Default: `"user"`        |
| hashed_pw   | String  |                          |

Roles: `user`, `manager`

When a user is deleted, all their assigned tasks are deleted via cascade.

### Task

| Column       | Type    | Constraints                 |
|--------------|---------|-----------------------------|
| id           | Integer | Primary key, indexed        |
| title        | String  | Indexed                     |
| description  | String  |                             |
| is_completed | Boolean | Default: `false`            |
| owner_id     | Integer | Foreign key -> `users.id`   |

---

## API Reference

### Users

#### POST /users/register

Register a new user. The role defaults to `"user"`.

Request body:
```json
{
  "email": "john@example.com",
  "username": "john",
  "password": "strongpassword",
  "confirm_password": "strongpassword"
}
```

Response `200 OK`:
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "john"
}
```

---

#### POST /users/login

Authenticate a user and receive a JWT access token.

Request body (`application/x-www-form-urlencoded`):
```
username=john
password=strongpassword
```

Response `200 OK`:
```json
{
  "access_token": "<jwt_token>",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "john@example.com",
    "username": "john"
  }
}
```

---

#### GET /users/me/{user_id}

Get account information for a given user. Requires authentication.

Headers:
```
Authorization: Bearer <jwt_token>
```

Response `200 OK`:
```json
{
  "id": 1,
  "email": "john@example.com",
  "username": "john"
}
```

---

#### GET /users/tasks

Get all tasks assigned to the authenticated user.

Headers:
```
Authorization: Bearer <jwt_token>
```

Response `200 OK`:
```json
[
  {
    "id": 1,
    "title": "Write documentation",
    "description": "Write the project README",
    "is_completed": false,
    "owner_id": 1
  }
]
```

---

### Manager

All endpoints under `/manager` require the authenticated user to have the `manager` role.

#### POST /manager/task/create

Create and assign a task to a user.

Headers:
```
Authorization: Bearer <jwt_token>
```

Request body:
```json
{
  "title": "Fix login bug",
  "description": "The login endpoint returns 500 under load",
  "is_completed": false,
  "assigned_user_id": 2
}
```

Response `200 OK`:
```json
{
  "id": 3,
  "title": "Fix login bug",
  "description": "The login endpoint returns 500 under load",
  "is_completed": false,
  "owner_id": 2
}
```

---

#### DELETE /manager/task/delete/{task_id}

Delete a task by ID.

Headers:
```
Authorization: Bearer <jwt_token>
```

Response `200 OK`:
```json
{
  "message": "Task has been deleted"
}
```

---

## Authentication

The API uses OAuth2 with Bearer tokens (JWT).

1. Call `POST /users/login` with your credentials.
2. Use the returned `access_token` in subsequent requests via the `Authorization` header:
   ```
   Authorization: Bearer <token>
   ```

Tokens expire after the duration configured in `ACCESS_TOKEN_EXPIRE_MINUTES` (default: 30 minutes).

Tokens are signed using HS256 with the `SECRET_KEY` defined in your environment.

---

## Role-Based Access Control

There are two roles in the system:

| Role    | Description                                              |
|---------|----------------------------------------------------------|
| user    | Default role. Can read their own tasks and account info. |
| manager | Can create and delete tasks for any user.                |

The `manager` role must be assigned manually in the database. Registration always assigns the `user` role.

Attempting to access a manager endpoint as a regular user returns:
```json
{
  "detail": "You are not a manager, cant create tasks"
}
```

---

## Getting Started

### Prerequisites

- Python 3.12+
- Docker and Docker Compose
- [uv](https://github.com/astral-sh/uv) or pip for dependency management

### 1. Clone the repository

```bash
git clone <repository-url>
cd teamsync-api
```

### 2. Create a virtual environment and install dependencies

Using uv:
```bash
uv venv
source .venv/bin/activate
uv sync
```

Using pip:
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3. Configure environment variables

Create a `.env` file in the project root:
```env
DATABASE_URL=postgresql://admin:admin123@localhost:5432/teamsyncdb
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### 4. Start the database

```bash
docker compose up -d
```

### 5. Run migrations

```bash
alembic upgrade head
```

### 6. Start the server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

Interactive documentation is available at `http://localhost:8000/docs`.

---

## Environment Variables

| Variable                  | Required | Default      | Description                          |
|---------------------------|----------|--------------|--------------------------------------|
| DATABASE_URL              | Yes      | —            | PostgreSQL connection string         |
| SECRET_KEY                | Yes      | —            | Key used to sign JWT tokens          |
| ALGORITHM                 | No       | `HS256`      | JWT signing algorithm                |
| ACCESS_TOKEN_EXPIRE_MINUTES | No     | `30`         | Token expiration time in minutes     |

---

## Database Migrations

Migrations are managed with Alembic.

Create a new migration after modifying models:
```bash
alembic revision --autogenerate -m "describe your change"
```

Apply all pending migrations:
```bash
alembic upgrade head
```

Revert the last migration:
```bash
alembic downgrade -1
```

View migration history:
```bash
alembic history
```

Check current database revision:
```bash
alembic current
```

---

## Running the Application

Development server with auto-reload:
```bash
uvicorn app.main:app --reload
```

Production server:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```
