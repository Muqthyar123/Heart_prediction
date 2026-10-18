import uuid
from datetime import datetime, timezone
from app.extensions import db


class HospitalSummaryPreference(db.Model):
    __tablename__ = "hospital_summary_preferences"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)

    include_profile = db.Column(db.Boolean, default=True, nullable=False)
    include_emergency_contact = db.Column(db.Boolean, default=True, nullable=False)
    include_allergies = db.Column(db.Boolean, default=True, nullable=False)
    include_medications = db.Column(db.Boolean, default=True, nullable=False)
    include_surgeries = db.Column(db.Boolean, default=True, nullable=False)
    include_family_history = db.Column(db.Boolean, default=True, nullable=False)
    include_heart_predictions = db.Column(db.Boolean, default=True, nullable=False)
    include_lifestyle_assessments = db.Column(db.Boolean, default=True, nullable=False)
    max_heart_records = db.Column(db.Integer, default=5, nullable=False)
    max_lifestyle_records = db.Column(db.Integer, default=5, nullable=False)

    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    user = db.relationship("User", back_populates="hospital_summary_preference")

    def to_dict(self):
        return {
            "include_profile": self.include_profile,
            "include_emergency_contact": self.include_emergency_contact,
            "include_allergies": self.include_allergies,
            "include_medications": self.include_medications,
            "include_surgeries": self.include_surgeries,
            "include_family_history": self.include_family_history,
            "include_heart_predictions": self.include_heart_predictions,
            "include_lifestyle_assessments": self.include_lifestyle_assessments,
            "max_heart_records": self.max_heart_records,
            "max_lifestyle_records": self.max_lifestyle_records,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }


class ConsentRecord(db.Model):
    __tablename__ = "consent_records"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)

    action = db.Column(db.String(80), nullable=False)  # 'share_summary', 'download_pdf', 'export_records'
    consent_given = db.Column(db.Boolean, default=True, nullable=False)
    consent_text = db.Column(db.Text, nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(255), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    user = db.relationship("User", back_populates="consent_records")

    def to_dict(self):
        return {
            "consent_id": self.id,
            "user_id": self.user_id,
            "action": self.action,
            "consent_given": self.consent_given,
            "consent_text": self.consent_text,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
