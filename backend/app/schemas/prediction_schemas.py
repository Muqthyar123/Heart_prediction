from marshmallow import Schema, fields, validate


class HeartPredictionInputSchema(Schema):
    age = fields.Integer(required=True, validate=validate.Range(min=1, max=120))
    sex = fields.Integer(required=True, validate=validate.OneOf([0, 1]))
    cp = fields.Integer(required=True, validate=validate.OneOf([0, 1, 2, 3]))
    trestbps = fields.Float(required=True, validate=validate.Range(min=50.0, max=260.0))
    chol = fields.Float(required=True, validate=validate.Range(min=80.0, max=650.0))
    fbs = fields.Integer(required=True, validate=validate.OneOf([0, 1]))
    restecg = fields.Integer(required=True, validate=validate.OneOf([0, 1, 2]))
    thalach = fields.Float(required=True, validate=validate.Range(min=50.0, max=250.0))
    exang = fields.Integer(required=True, validate=validate.OneOf([0, 1]))
    oldpeak = fields.Float(required=True, validate=validate.Range(min=0.0, max=10.0))
    slope = fields.Integer(required=True, validate=validate.OneOf([0, 1, 2]))
    ca = fields.Integer(required=True, validate=validate.OneOf([0, 1, 2, 3, 4]))
    thal = fields.Integer(required=True, validate=validate.OneOf([0, 1, 2, 3]))


class SinglePredictionRequestSchema(Schema):
    features = fields.Nested(HeartPredictionInputSchema, required=True)
    model_name = fields.String(load_default="hybrid_stacking")
    save_to_history = fields.Boolean(load_default=True)
    patient_identifier = fields.String(load_default=None, validate=validate.Length(max=60))
