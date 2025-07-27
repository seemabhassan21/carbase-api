from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import db, Car
from .car_schema import CarSchema

car_bp = Blueprint('car', __name__)
car_schema = CarSchema()
cars_schema = CarSchema(many=True)

# Utility: fetch object or 404
def get_or_404(model, id):
    obj = model.query.get(id)
    return obj if obj else None


# GET /cars (List + Filter + Pagination)
@car_bp.route('/', methods=['GET'])
@jwt_required()
def get_cars():
    query = Car.query

    for field in ['make', 'model']:
        val = request.args.get(field)
        if val:
            query = query.filter(getattr(Car, field).ilike(f"%{val}%"))

    year = request.args.get('year', type=int)
    if year is not None:
        query = query.filter(Car.year == year)

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    paginated = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "cars": cars_schema.dump(paginated.items),
        "total": paginated.total,
        "page": paginated.page,
        "pages": paginated.pages
    })


# GET /cars/<id>
@car_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_car(id):
    car = get_or_404(Car, id)
    return car_schema.jsonify(car) if car else jsonify({"error": "Not found"}), 404


# POST /cars
@car_bp.route('/', methods=['POST'])
@jwt_required()
def create_car():
    data = request.get_json()
    if (errors := car_schema.validate(data)):
        return jsonify(errors), 400

    if Car.query.filter_by(**data).first():
        return jsonify({"error": "Car already exists"}), 409

    car = Car(**data)
    db.session.add(car)
    db.session.commit()
    return car_schema.jsonify(car), 201


# PUT /cars/<id>
@car_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_car(id):
    car = get_or_404(Car, id)
    if not car:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    if (errors := car_schema.validate(data)):
        return jsonify(errors), 400

    for key, value in data.items():
        setattr(car, key, value)

    db.session.commit()
    return car_schema.jsonify(car)


# PATCH /cars/<id>
@car_bp.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def patch_car(id):
    car = get_or_404(Car, id)
    if not car:
        return jsonify({"error": "Not found"}), 404

    data = request.get_json()
    for key in ['make', 'model', 'year']:
        if key in data:
            setattr(car, key, data[key])

    db.session.commit()
    return car_schema.jsonify(car)


# DELETE /cars/<id>
@car_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_car(id):
    car = get_or_404(Car, id)
    if not car:
        return jsonify({"error": "Not found"}), 404

    db.session.delete(car)
    db.session.commit()
    return jsonify({"message": "Car deleted successfully"}), 200
