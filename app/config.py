import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET", "jwt-secret")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///cars.db'
    SQLALCHEMY_TRACK_MODIFICATION = False
    CELERY_BROKER_URL = 'redis://localhost:6379/0'
    result_backend = "redis://redis:6379/0"

    CAR_API_URL = 'https://parseapi.back4app.com/classes/Car_Model_List?limit=10000'
    CAR_API_HEADERS = {
        'X-Parse-Application-Id': 'hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z',  # This is the fake app's application id
        'X-Parse-Master-Key': 'SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW'  # This is the fake app's readonly master key
    }
