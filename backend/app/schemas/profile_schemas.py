from marshmallow import Schema, fields, validate


class EmergencyContactSchema(Schema):
    name = fields.String(load_default=None, validate=validate.Length(max=150))
    phone = fields.String(load_default=None, validate=validate.Length(max=30))
    relation = fields.String(load_default=None, validate=validate.Length(max=60))


class InsuranceSchema(Schema):
    provider = fields.String(load_default=None, validate=validate.Length(max=150))
    policy_number = fields.String(load_default=None, validate=validate.Length(max=100))


class PatientProfileSchema(Schema):
    full_name = fields.String(load_default=None, validate=validate.Length(max=150))
    date_of_birth = fields.Date(load_default=None)
    gender = fields.String(load_default=None, validate=validate.OneOf(["Male", "Female", "Other", "male", "female", "other"]))
    phone_number = fields.String(load_default=None, validate=validate.Length(max=30))
    contact_email = fields.Email(load_default=None)
    address = fields.String(load_default=None, validate=validate.Length(max=255))
    city = fields.String(load_default=None, validate=validate.Length(max=100))
    state = fields.String(load_default=None, validate=validate.Length(max=100))

    emergency_contact = fields.Nested(EmergencyContactSchema, load_default=None)

    blood_group = fields.String(
        load_default=None,
        validate=validate.OneOf(["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-", ""]),
    )
    height_cm = fields.Float(load_default=None, validate=validate.Range(min=30, max=280))
    weight_kg = fields.Float(load_default=None, validate=validate.Range(min=10, max=400))

    known_allergies = fields.String(load_default=None)
    existing_medical_conditions = fields.String(load_default=None)
    current_medications = fields.String(load_default=None)
    previous_surgeries = fields.String(load_default=None)
    family_history_heart_disease = fields.Boolean(load_default=False)

    preferred_hospital = fields.String(load_default=None, validate=validate.Length(max=150))
    preferred_doctor = fields.String(load_default=None, validate=validate.Length(max=150))
    insurance = fields.Nested(InsuranceSchema, load_default=None)
    patient_identifier = fields.String(load_default=None, validate=validate.Length(max=50))
