# BLOG_API_PROJECT

A production-ready RESTful Blog API built step-by-step following the **FastAPI Full Course by Mohit Decodes**.

---

## 🛠️ Features & Progress

### 1. Basic Setup & Core Concepts
- [x] Virtual Environment & FastAPI Setup
- [ ] Swagger UI & ReDoc API Documentation
- [ ] Path & Query Parameters
- [ ] Request Body & Pydantic Data Validation

### 2. Database & CRUD Operations
- [ ] Database Connection setup using SQLAlchemy
- [ ] Database Models (Blogs & Users tables)
- [ ] Full CRUD APIs for Blog Posts (Create, Read, Update, Delete)

### 3. Advanced Features & Security
- [ ] User Signup & Password Hashing (Bcrypt)
- [ ] JWT Authentication & Login API
- [ ] Router Refactoring & Clean Architecture (APIRouter)
- [ ] Dependency Injection & Repository Pattern

---

## 💻 Tech Stack

- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Database:** SQLite / PostgreSQL
- **ORM:** SQLAlchemy
- **Data Validation:** Pydantic
- **Authentication:** OAuth2 with Password Bearer & JWT Tokens
- **Server:** Uvicorn

---

## 📂 Project Structure

```text
BLOG_API_PROJECT/
├── repository/          # Database queries & CRUD logic
│   ├── blog.py
│   └── user.py
├── routers/             # API route controllers
│   ├── authentication.py
│   ├── blog.py
│   └── user.py
├── database.py          # SQLAlchemy engine & session setup
├── hashing.py           # Password hashing utilities
├── main.py              # Application entry point
├── models.py            # SQLAlchemy database models
├── oauth2.py           # OAuth2 authentication dependency
├── schemas.py           # Pydantic validation schemas
└── token.py             # JWT token handling (Create & Verify)
