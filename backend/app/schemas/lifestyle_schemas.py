from marshmallow import Schema, fields, validate


class LifestyleInputSchema(Schema):
    activity = fields.Integer(required=True, validate=validate.OneOf([1, 2, 3, 4]))
    diet = fields.Integer(required=True, validate=validate.OneOf([1, 2, 3, 4]))
    smoking = fields.Integer(required=True, validate=validate.OneOf([1, 2, 3, 4]))
    alcohol = fields.Integer(required=True, validate=validate.OneOf([1, 2, 3, 4]))
    sleep = fields.Integer(required=True, validate=validate.OneOf([1, 2, 3, 4]))
    stress = fields.Integer(required=True, validate=validate.OneOf([1, 2, 3, 4]))
    weight = fields.Integer(required=True, validate=validate.OneOf([1, 2, 3, 4]))
    save_to_history = fields.Boolean(load_default=True)
