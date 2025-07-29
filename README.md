# CarBase API

A Flask-based backend API for managing car registration data. It fetches data from an external car API, stores it in a local SQLite database, and supports secure user authentication using JWT. Periodic syncing is handled by Celery and Redis.

---

## Features

- JWT-based user authentication (`/api/signup`, `/api/login`)
- CRUD operations on car entries (`/api/cars`)
- External car model API integration
- Scheduled background syncing every 5 minutes (Celery Beat)
- Token expiration & signature validation
- SQLite3 database with SQLAlchemy ORM
- Celery worker and beat for scheduled jobs
- Dockerized with Redis for async tasks
- Modular Flask project structure

---

## API Endpoints

| Method | Route                       | Auth | Description                |
|--------|-----------------------------|------|----------------------------|
| POST   | `/api/signup`               | No   | Register a new user        |
| POST   | `/api/login`                | No   | Login and get JWT token    |
| GET    | `/api/cars`                 | Yes  | List all cars (with filters)|
| GET    | `/api/cars/<id>`            | Yes  | Get car by ID              |
| POST   | `/api/cars`                 | Yes  | Create a new car           |
| PATCH  | `/api/cars/<id>`            | Yes  | Update a car by ID         |
| PUT    | `/api/cars/<id>`            | Yes  | Replace a car by ID        |
| DELETE | `/api/cars/<id>`            | Yes  | Delete car by ID           |
| POST   | `/api/cars/sync-cars`       | Yes  | Trigger background sync    |

Filters supported on `/api/cars` via query params: `make`, `model`, `year`, `page`, `limit`.

Example:
```
GET /api/cars?make=Toyota&year=2020&page=2&limit=20
```

---

## Project Setup (Local)

1. **Clone and create environment**
   ```bash
   git clone https://github.com/yourusername/carbase-api.git
   cd carbase-api
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. **Create the .env file (required before first run)**
   ```env
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret
   SQLALCHEMY_DATABASE_URI=sqlite:///instance/cars.db
   CAR_API_ID=your-parse-app-id
   CAR_API_KEY=your-parse-master-key
   CELERY_BROKER_URL=redis://localhost:6379/0
   CELERY_RESULT_BACKEND=redis://localhost:6379/0
   ```
   **Important:** Ensure these secrets are set explicitly. Otherwise, random values will be generated inside the container and invalidate tokens on every rebuild.
3. **Ensure the instance directory exists**
   ```bash
   mkdir -p instance
   chmod 777 instance
   ```
4. **Initialize the database**
   ```bash
   flask shell
   >>> from app.extensions import db
   >>> db.create_all()
   >>> exit()
   ```
5. **Run services manually (non-Docker)**
   - Redis:
     ```bash
     redis-server
     ```
   - Flask app:
     ```bash
     python run.py
     ```
   - Celery worker:
     ```bash
     celery -A app.tasks.celery_worker.celery worker --loglevel=info
     ```
   - Celery beat (optional, for periodic syncing):
     ```bash
     celery -A app.tasks.celery_worker.celery beat --loglevel=info
     ```

---

## Docker Setup

1. **Create .env file (required before build)**
   ```env
   SECRET_KEY=your-secret-key
   JWT_SECRET_KEY=your-jwt-secret
   SQLALCHEMY_DATABASE_URI=sqlite:////app/instance/cars.db
   CAR_API_ID=your-parse-app-id
   CAR_API_KEY=your-parse-master-key
   CELERY_BROKER_URL=redis://redis:6379/0
   CELERY_RESULT_BACKEND=redis://redis:6379/0
   ```
   **Warning:** If JWT_SECRET_KEY is missing, the container will auto-generate a random key, invalidating all previously issued tokens. Always define it before running Docker!
2. **Ensure the instance directory exists on your host**
   ```bash
   mkdir -p instance
   chmod 777 instance
   ```
3. **Build and start all services**
   ```bash
   docker-compose up --build
   ```

---

## Interact with the API

Below are example requests for all major endpoints. Replace `<your_token>` with the JWT you receive after login.

### Sign Up
```bash
curl -X POST http://localhost:5000/api/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "user1", "email": "user@example.com", "password": "pass123"}'
```

### Login
```bash
curl -X POST http://localhost:5000/api/login \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "pass123"}'
```

### Get All Cars (with optional filters)
```bash
curl -X GET "http://localhost:5000/api/cars?make=Toyota&year=2021&page=1&limit=10" \
  -H "Authorization: Bearer <your_token>"
```

### Get Car by ID
```bash
curl -X GET http://localhost:5000/api/cars/1 \
  -H "Authorization: Bearer <your_token>"
```

### Create a New Car
```bash
curl -X POST http://localhost:5000/api/cars \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_token>" \
  -d '{"make": "Toyota", "model": "Corolla", "year": 2021}'
```

### Update a Car (PATCH)
```bash
curl -X PATCH http://localhost:5000/api/cars/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_token>" \
  -d '{"model": "Camry"}'
```

### Replace a Car (PUT)
```bash
curl -X PUT http://localhost:5000/api/cars/1 \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <your_token>" \
  -d '{"make": "Honda", "model": "Civic", "year": 2022}'
```

### Delete a Car
```bash
curl -X DELETE http://localhost:5000/api/cars/1 \
  -H "Authorization: Bearer <your_token>"
```

### Trigger Car Data Sync
```bash
curl -X POST http://localhost:5000/api/cars/sync-cars \
  -H "Authorization: Bearer <your_token>"
```

---

## Authentication

This project uses JWT-based authentication. Tokens must be included in the Authorization header as:

```
Authorization: Bearer <your_jwt_token>
```

After registering or logging in, copy the token from the response and include it in every protected request.

---

## Periodic Syncing

Every 5 minutes, Celery Beat triggers `sync_cars` to fetch car models from the external API and update the local DB.

Check logs in:
```
logs/sync_cars.log
```

---

## Error Handling

The API returns standard HTTP status codes with descriptive messages:
- `400` – Bad Request (validation failed)
- `401` – Unauthorized (missing or invalid token)
- `404` – Not Found (car or route not found)
- `409` – Conflict (duplicate car entry)
- `500` – Server Error (unexpected failures)

---

## Secret Management

All sensitive configuration (secrets, database URIs, API keys) should be placed in a `.env` file and loaded automatically. Example:

```
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
SQLALCHEMY_DATABASE_URI=sqlite:///instance/cars.db
CAR_API_ID=your-parse-app-id
CAR_API_KEY=your-parse-master-key
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

---

## Project Structure

```
carbase-api/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── extensions.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── car.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── auth_routes.py
│   │   │   └── user_schema.py
│   │   └── cars/
│   │       ├── __init__.py
│   │       ├── car_routes.py
│   │       └── car_schema.py
│   ├── tasks/
│   │   ├── __init__.py
│   │   ├── celery_worker.py
│   │   └── sync_cars.py
│   └── utils/
│       ├── __init__.py
│       └── auth.py
├── run.py
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .gitignore
└── README.md
```

**Note:** The following directories are created at runtime and excluded from Git:
- `instance/` - Contains SQLite database (created automatically)
- `logs/` - Contains application logs (created automatically)
- `.env` - Environment variables (not committed for security)

---

## Testing JWT

You can use [jwt.io](https://jwt.io/) to decode JWTs, but you must paste your JWT_SECRET_KEY under the "Verify Signature" section to validate it.

---

## Cleanup & Rebuild (Docker)

To completely reset:
Want a fresh restart of docker services follow the commands below 
```bash
docker-compose down -v
docker system prune -af
rm -rf instance/*.db
rm -rf logs/*
docker-compose up --build
```

---

## Maintainers

Seemab Hassan – Backend Intern

Project designed to demonstrate Flask + Celery + Docker integration with a clean modular codebase.

---

## Notes

- Don’t forget to map ports: 5000 (Flask) and 6379 (Redis)
- SQLite file and .env are persisted via volumes
- Secret keys must remain consistent across container rebuilds

## Troubleshooting

### Common Issues:


1. **JWT Token Issues**:
   - Ensure `JWT_SECRET_KEY` is consistent across rebuilds
   - Tokens get expire after 15 minutes so make sure to  get new ones via `/api/login`

2. **Database Not Found**:
   ```bash
   # Ensure instance directory exists
   mkdir -p instance
   chmod 777 instance
   ```

3. **Redis Connection Failed**:
   ```bash
   # Check if Redis is running
   docker-compose logs redis
   ```
