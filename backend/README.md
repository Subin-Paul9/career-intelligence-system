# Career Intelligence Backend

## Framework

FastAPI

---

## Python Version

Python 3.12+

---

## Backend Stack

- FastAPI
- SQLAlchemy
- PostgreSQL
- Alembic
- Python-JOSE (JWT)
- Passlib
- bcrypt
- Pydantic
- Uvicorn

---

## Installation

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

#### Windows

```bash
venv\Scripts\activate
```

#### Linux

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Development Server

```bash
uvicorn main:app --reload
```

---

## Application URLs

### Backend

```
http://127.0.0.1:8000
```

### Swagger UI

```
http://127.0.0.1:8000/docs
```

### ReDoc

```
http://127.0.0.1:8000/redoc
```

---

## Database

**Database:** PostgreSQL

**Database Name**

```
career_intelligence_db
```

---

# Phase 3 – Authentication & User Management

## Implemented Features

### Authentication

- ✅ User Registration
- ✅ User Login
- ✅ JWT Authentication
- ✅ Password Hashing (bcrypt)

### Database

- ✅ PostgreSQL Integration
- ✅ SQLAlchemy ORM
- ✅ User Model
- ✅ Default Administrator Account

### User Management

- ✅ Protected APIs
- ✅ Get User Profile
- ✅ Update User Profile
- ✅ Soft Delete User Account

---

# API Endpoints

## Authentication APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| POST | `/api/auth/register` | Register a new user |
| POST | `/api/auth/login` | Authenticate user and return JWT access token |

## User APIs

| Method | Endpoint | Description |
|---------|----------|-------------|
| GET | `/api/users/profile` | Retrieve authenticated user's profile |
| PUT | `/api/users/profile` | Update authenticated user's profile |
| DELETE | `/api/users/profile` | Soft delete (deactivate) authenticated user's account |

---

# Authentication Flow

```text
User Registration
        │
        ▼
Password Hashing (bcrypt)
        │
        ▼
Store User in PostgreSQL
        │
        ▼
User Login
        │
        ▼
JWT Access Token Generated
        │
        ▼
Access Protected APIs
```

---

# Project Structure

```text
backend/
│
├── app/
│   ├── config/
│   ├── core/
│   ├── database/
│   ├── dependencies/
│   ├── models/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── static/
│   ├── templates/
│   └── utils/
│
├── alembic/
├── main.py
├── requirements.txt
└── README.md
```

---

# Technologies Used

- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Pydantic
- Passlib
- bcrypt
- Python-JOSE (JWT)
- Swagger UI (OpenAPI)
- Uvicorn

---

# Phase 3 Completion Checklist

- ✅ Database Connection
- ✅ PostgreSQL Integration
- ✅ SQLAlchemy ORM
- ✅ User Registration
- ✅ Password Hashing (bcrypt)
- ✅ Login API
- ✅ JWT Token Generation
- ✅ JWT Token Verification
- ✅ Protected API Authentication
- ✅ User Profile APIs
- ✅ Soft Delete Functionality
- ✅ Default Administrator Account
- ✅ Administrator Login Tested

---

# Status

**Phase 3 Completed Successfully** 🎉

The backend authentication module is fully functional and includes:

- Secure user registration
- Password hashing using bcrypt
- JWT-based authentication
- Protected REST APIs
- User profile management
- PostgreSQL database integration
- Default administrator account
- Interactive API documentation using Swagger UI