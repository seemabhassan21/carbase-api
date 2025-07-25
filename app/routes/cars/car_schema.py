# app/schemas/car_schema.py

from app import ma
from app.models import Car

class CarSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Car
        load_instance = True

