
from marshmallow import Schema, fields, validate

class CarSchema(Schema):
    id = fields.Integer(dump_only=True)
    make = fields.String(required=True, validate=validate.Length(min=1, max=100))
    model = fields.String(required=True, validate=validate.Length(min=1, max=100))
    year = fields.Integer(required=True, validate=validate.Range(min=1900, max=2030))
    created_at = fields.DateTime(dump_only=True)

