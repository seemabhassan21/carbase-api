from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.models import Car
from app.extensions import db
from .car_schema import CarSchema

car_bp = Blueprint('car', __name__)
car_schema = CarSchema()
cars_schema = CarSchema(many=True)

# --- Utility Functions ---

def get_car_or_404(car_id):
    car = Car.query.get(car_id)
    if not car:
        return jsonify({"error": "Car not found"}), 404
    return car

def validate_car_data(data, partial=False):
    errors = car_schema.validate(data, partial=partial)
    if errors:
        return jsonify({"validation_errors": errors}), 400
    return None

def car_exists(make, model, year):
    return Car.query.filter_by(make=make, model=model, year=year).first() is not None

# --- Routes ---

@car_bp.route('/', methods=['GET'])
@jwt_required()
def list_cars():
    query = Car.query

    filters = {
        'make': request.args.get('make'),
        'model': request.args.get('model'),
        'year': request.args.get('year', type=int)
    }

    if filters['make']:
        query = query.filter(Car.make.ilike(f"%{filters['make']}%"))
    if filters['model']:
        query = query.filter(Car.model.ilike(f"%{filters['model']}%"))
    if filters['year']:
        query = query.filter(Car.year == filters['year'])

    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    paginated = query.paginate(page=page, per_page=limit, error_out=False)

    return jsonify({
        "cars": cars_schema.dump(paginated.items),
        "total": paginated.total,
        "page": paginated.page,
        "pages": paginated.pages
    })

@car_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def retrieve_car(id):
    car = get_car_or_404(id)
    if isinstance(car, tuple):  # error tuple
        return car
    return jsonify(car_schema.dump(car))

@car_bp.route('/', methods=['POST'])
@jwt_required()
def create_car():
    data = request.get_json()

    error = validate_car_data(data)
    if error:
        return error

    make, model, year = data.get('make'), data.get('model'), data.get('year')
    if car_exists(make, model, year):
        return jsonify({"error": "Car with same make, model and year already exists"}), 409

    new_car = Car(**data)
    db.session.add(new_car)
    db.session.commit()

    return jsonify(car_schema.dump(new_car)), 201

@car_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def replace_car(id):
    car = get_car_or_404(id)
    if isinstance(car, tuple):
        return car

    data = request.get_json()
    error = validate_car_data(data)
    if error:
        return error

    for field in ['make', 'model', 'year']:
        setattr(car, field, data.get(field))

    db.session.commit()
    return jsonify(car_schema.dump(car))

@car_bp.route('/<int:id>', methods=['PATCH'])
@jwt_required()
def update_car(id):
    car = get_car_or_404(id)
    if isinstance(car, tuple):
        return car

    data = request.get_json()
    error = validate_car_data(data, partial=True)
    if error:
        return error

    for field, value in data.items():
        if hasattr(car, field):
            setattr(car, field, value)

    db.session.commit()
    return jsonify(car_schema.dump(car))

@car_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_car(id):
    car = get_car_or_404(id)
    if isinstance(car, tuple):
        return car

    db.session.delete(car)
    db.session.commit()
    return jsonify({"message": "Car deleted successfully"}), 200

@car_bp.route('/sync-cars', methods=['POST'])
@jwt_required()
def sync_cars_endpoint():
    from app.tasks.sync_cars import sync_cars
    sync_cars.delay()
    return jsonify({"message": "Car sync started"}), 200
