from .auth_routes import auth_bp
from .car_routes import car_bp

all_blueprints = [
    (auth_bp, '/api'),         # login, register, etc.
    (car_bp, '/api/cars')      # all car-related endpoints
]
