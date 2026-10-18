from marshmallow import Schema, fields


class SummaryPreferenceSchema(Schema):
    include_profile = fields.Boolean(load_default=True)
    include_emergency_contact = fields.Boolean(load_default=True)
    include_allergies = fields.Boolean(load_default=True)
    include_medications = fields.Boolean(load_default=True)
    include_surgeries = fields.Boolean(load_default=True)
    include_family_history = fields.Boolean(load_default=True)
    include_heart_predictions = fields.Boolean(load_default=True)
    include_lifestyle_assessments = fields.Boolean(load_default=True)
    max_heart_records = fields.Integer(load_default=5)
    max_lifestyle_records = fields.Integer(load_default=5)


class ShareSummarySchema(Schema):
    consent = fields.Boolean(required=True)
    recipient_email = fields.Email(load_default=None)
    recipient_name = fields.String(load_default=None)
    purpose = fields.String(load_default="Doctor consultation clinical reference")
