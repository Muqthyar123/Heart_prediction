import uuid
from datetime import datetime, timezone
from app.extensions import db


class PatientProfile(db.Model):
    __tablename__ = "patient_profiles"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)

    # Demographic & Contact Fields
    full_name = db.Column(db.String(150), nullable=True)
    date_of_birth = db.Column(db.Date, nullable=True)
    gender = db.Column(db.String(30), nullable=True)
    phone_number = db.Column(db.String(30), nullable=True)
    contact_email = db.Column(db.String(255), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(100), nullable=True)
    state = db.Column(db.String(100), nullable=True)

    # Emergency Contact
    emergency_contact_name = db.Column(db.String(150), nullable=True)
    emergency_contact_phone = db.Column(db.String(30), nullable=True)
    emergency_contact_relation = db.Column(db.String(60), nullable=True)

    # Clinical & Medical Background
    blood_group = db.Column(db.String(10), nullable=True)
    height_cm = db.Column(db.Float, nullable=True)
    weight_kg = db.Column(db.Float, nullable=True)
    known_allergies = db.Column(db.Text, nullable=True)
    existing_medical_conditions = db.Column(db.Text, nullable=True)
    current_medications = db.Column(db.Text, nullable=True)
    previous_surgeries = db.Column(db.Text, nullable=True)
    family_history_heart_disease = db.Column(db.Boolean, default=False, nullable=True)

    # Care Preferences & System Identifier
    preferred_hospital = db.Column(db.String(150), nullable=True)
    preferred_doctor = db.Column(db.String(150), nullable=True)
    insurance_provider = db.Column(db.String(150), nullable=True)
    insurance_policy_number = db.Column(db.String(100), nullable=True)
    patient_identifier = db.Column(db.String(50), nullable=True)
    photo_filename = db.Column(db.String(255), nullable=True)

    completion_percentage = db.Column(db.Integer, default=0, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationship
    user = db.relationship("User", back_populates="profile")

    def calculate_completion(self) -> int:
        """
        Calculates profile completion percentage based on 10 key sections:
        1. Name & DOB (15%)
        2. Gender (10%)
        3. Phone / Email (10%)
        4. Address / City / State (10%)
        5. Emergency Contact (15%)
        6. Blood Group (10%)
        7. Height & Weight (10%)
        8. Medical history / conditions / allergies (10%)
        9. Medications / Surgeries (5%)
        10. Family history (5%)
        """
        score = 0
        if self.full_name and self.date_of_birth:
            score += 15
        elif self.full_name or self.date_of_birth:
            score += 8

        if self.gender:
            score += 10

        if self.phone_number or self.contact_email:
            score += 10

        if self.address or (self.city and self.state):
            score += 10

        if self.emergency_contact_name and self.emergency_contact_phone:
            score += 15
        elif self.emergency_contact_name or self.emergency_contact_phone:
            score += 7

        if self.blood_group:
            score += 10

        if self.height_cm and self.weight_kg:
            score += 10
        elif self.height_cm or self.weight_kg:
            score += 5

        if self.existing_medical_conditions or self.known_allergies:
            score += 10

        if self.current_medications or self.previous_surgeries:
            score += 5

        if self.family_history_heart_disease is not None:
            score += 5

        self.completion_percentage = min(score, 100)
        return self.completion_percentage

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "full_name": self.full_name,
            "date_of_birth": self.date_of_birth.isoformat() if self.date_of_birth else None,
            "gender": self.gender,
            "phone_number": self.phone_number,
            "contact_email": self.contact_email,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "emergency_contact": {
                "name": self.emergency_contact_name,
                "phone": self.emergency_contact_phone,
                "relation": self.emergency_contact_relation,
            },
            "blood_group": self.blood_group,
            "height_cm": self.height_cm,
            "weight_kg": self.weight_kg,
            "known_allergies": self.known_allergies,
            "existing_medical_conditions": self.existing_medical_conditions,
            "current_medications": self.current_medications,
            "previous_surgeries": self.previous_surgeries,
            "family_history_heart_disease": self.family_history_heart_disease,
            "preferred_hospital": self.preferred_hospital,
            "preferred_doctor": self.preferred_doctor,
            "insurance": {
                "provider": self.insurance_provider,
                "policy_number": self.insurance_policy_number,
            },
            "patient_identifier": self.patient_identifier,
            "photo_filename": self.photo_filename,
            "completion_percentage": self.completion_percentage,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }
