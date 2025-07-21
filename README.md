# Carbase API

Carbase API is a backend Flask-based RESTful service for managing and querying car model data.This project is designed with modular architecture, background processing (Celery), and clean API design in mind.
The API supports user authentication, secure endpoints via JWT, dynamic filtering with pagination and data synchronization from an external car database.

---

## 🚀 Features

- User Registration & Login with JWT
- CRUD operations on car models
- Pagination and filtering (make, model, year)
- External API integration
- Background data sync with Celery
- SQLite database
- Clean architecture with modular Flask blueprint structure

---

## 🛠 Tech Stack

- Python 3.11+
- Flask
- SQLAlchemy (ORM)
- Flask-JWT-Extended
- Celery + Redis (Background Tasks)
- Marshmallow (Validation)
- SQLite (Local DB)
- Requests (External API calls)

---

## 📦 Setup Instructions

```bash
# Clone the repository
git clone https://github.com/yourusername/carbase-api.git
cd carbase-api

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the Flask API
flask run

# Optional: Start Celery worker (in separate terminal)
celery -A celery_worker.celery worker --loglevel=info

```

## 🔐 Authentication
This project uses JWT-based authentication. Tokens must be included in the Authorization header as:

```
Authorization: Bearer <your_jwt_token>
```

After registering or logging in, copy the token from the response and include it in every protected request.

## 📁 API Endpoints
### 👤 Auth Endpoints


| Method | Endpoint        | Description         | Auth Required |
|--------|-----------------|---------------------|---------------|
| POST   | `/api/signin  ` | Register new user   | ❌            |
| POST   | `/api/login`    | Log in, get JWT     | ❌            |

### 🚗 Car Endpoints

| Method | Endpoint         | Description                    | Auth Required |
|--------|------------------|--------------------------------|---------------|
| GET    | `/api/cars`      | List cars (with filters)       | ✅            |
| POST   | `/api/cars`      | Add a new car                  | ✅            |
| GET    | `/api/cars/<id>` | Get details of a car by ID     | ✅            |
| PUT    | `/api/cars/<id>` | Fully replace a car by ID      | ✅            |
| PATCH  | `/api/cars/<id>` | Partially update a car by ID   | ✅            |
| DELETE | `/api/cars/<id>` | Delete a car by ID             | ✅            |


✅ Filters supported on /api/cars via query params:

- make

- model

- year

- page

- limit

Example:

```
GET /api/cars?make=Toyota&year=2020&page=2&limit=20

```

## 🧪 Sample API Calls
These examples help you quickly test the API using curl. Replace <your_token> with the actual JWT you get after login.

### 🔐 Login
```
curl -X POST http://localhost:5000/api/login \
-H "Content-Type: application/json" \
-d '{"email": "user@example.com", "password": "yourpassword"}'
```

### 🚗 Create a Car
```

curl -X POST http://localhost:5000/api/cars \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_token>" \
-d '{"make": "Toyota", "model": "Corolla", "year": 2021}'
```

### 📄 Get All Cars (With Filters)
```
curl -X GET "http://localhost:5000/api/cars?make=Toyota&year=2021&page=1&limit=10" \
-H "Authorization: Bearer <your_token>"

```

### 🛠 Update a Car (PUT)
```

curl -X PUT http://localhost:5000/api/cars/1 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_token>" \
-d '{"make": "Honda", "model": "Civic", "year": 2022}'
```


### 🛠 Partially Update a Car (PATCH)

```

curl -X PATCH http://localhost:5000/api/cars/1 \
-H "Content-Type: application/json" \
-H "Authorization: Bearer <your_token>" \
-d '{"model": "Accord"}'

```
### ❌ Delete a Car
```
curl -X DELETE http://localhost:5000/api/cars/1 \
-H "Authorization: Bearer <your_token>"

```

## 🔄 Syncing Cars from External API
Cars are synced using a Celery task that fetches data from Back4App’s car model list and stores it in the local database.



## 🚨 Error Handling

The API returns standard HTTP status codes with descriptive messages.

- `400` – Bad Request (Validation failed)
- `401` – Unauthorized (Missing or invalid token)
- `404` – Not Found (Car or route not found)
- `409` – Conflict (Duplicate car entry)
- `500` – Server Error (Unexpected failures)



## 🔑 Secret Management
Currently, the JWT secret key is hardcoded in your Flask config.

### 👉 Recommendation: Create a .env file for environment variables in production.

Example .env:

```

JWT_SECRET_KEY=your_super_secret_key
DATABASE_URL=sqlite:///app.db

```

Use python-dotenv to load .env in your app/__init__.py:

```
from dotenv import load_dotenv
load_dotenv()
```

## 🧪 Testing
Use Postman to test each endpoint. Don't forget to add your JWT token under Headers as:

```
Authorization: Bearer <your_token>
```

## ⚠️ Dev Notes

- Run Redis before starting Celery: `redis-server`
- Use `.env` to keep secrets out of version control
- Use `flask db init/migrate/upgrade` for managing DB migrations

## 📂 Project Structure


```
carbase-api/
├── app/
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   └── car_routes.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── car_schema.py
│   │   └── user_schema.py
│   ├── tasks/
│   │   └── sync_cars.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── config.py
│   │   └── extensions.py
│   └── models.py
├── instance/
├── migrations/
├── .venv/
├── celery_worker.py
├── requirement.txt
└── run.py

```

### 📘 Explanation

| Folder/File         | Purpose                                                      |
|---------------------|--------------------------------------------------------------|
| `app/routes/`       | Contains route handlers (auth and car endpoints).            |
| `app/schemas/`      | Marshmallow schemas for input/output validation.             |
| `app/tasks/`        | Background tasks (e.g., syncing with external APIs).         |
| `app/utils/`        | Utility code like JWT setup, config, and extensions.         |
| `app/models.py`     | SQLAlchemy models.                                           |
| `instance/`         | Holds environment-specific configs (if needed).              |
| `migrations/`       | Alembic database migrations.                                 |
| `.venv/`            | Virtual environment (usually excluded from Git).             |
| `celery_worker.py`  | Celery entry point for running background tasks.             |
| `requirement.txt`   | Project dependencies.                                        |
| `run.py`            | Flask app entry point.                                       |









## 📜 License

This project is licensed under the MIT License.

