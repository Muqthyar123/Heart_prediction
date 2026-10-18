import uuid
from datetime import datetime, timezone
from app.extensions import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Relationships
    profile = db.relationship("PatientProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    predictions = db.relationship("HeartPrediction", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    lifestyle_assessments = db.relationship(
        "LifestyleAssessment", back_populates="user", cascade="all, delete-orphan", lazy="dynamic"
    )
    bulk_jobs = db.relationship("BulkJob", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")
    hospital_summary_preference = db.relationship(
        "HospitalSummaryPreference", back_populates="user", uselist=False, cascade="all, delete-orphan"
    )
    consent_records = db.relationship("ConsentRecord", back_populates="user", cascade="all, delete-orphan", lazy="dynamic")

    def to_dict(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
            "is_active": self.is_active,
            "has_profile": self.profile is not None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
