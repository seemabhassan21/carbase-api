import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///cars.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Celery
    CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
    CELERY_RESULT_BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    
    # External API
    CAR_API_URL = "https://parseapi.back4app.com/classes/Car_Model_List?limit=10000"
    CAR_API_HEADERS = {
        'X-Parse-Application-Id': os.getenv("CAR_API_ID", "hlhoNKjOvEhqzcVAJ1lxjicJLZNVv36GdbboZj3Z"),
        'X-Parse-Master-Key': os.getenv("CAR_API_KEY", "SNMJJF0CZZhTPhLDIqGhTlUNV9r60M2Z5spyWfXW")
    }
