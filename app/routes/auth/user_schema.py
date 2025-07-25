# app/schemas/user_schema.py

from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=3))
    email = fields.Email(required=True)
    password = fields.String(required=True, load_only=True, validate=validate.Length(min=6))
