import json
import uuid
from datetime import datetime, timezone
from app.extensions import db


class BulkJob(db.Model):
    __tablename__ = "bulk_jobs"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)

    original_filename = db.Column(db.String(255), nullable=False)
    stored_filename = db.Column(db.String(255), nullable=False)

    total_rows = db.Column(db.Integer, default=0, nullable=False)
    valid_rows = db.Column(db.Integer, default=0, nullable=False)
    positive_predictions = db.Column(db.Integer, default=0, nullable=False)
    negative_predictions = db.Column(db.Integer, default=0, nullable=False)

    status = db.Column(db.String(30), default="pending", nullable=False)  # pending | processing | completed | failed
    error_message = db.Column(db.Text, nullable=True)
    result_filepath = db.Column(db.String(500), nullable=True)

    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)
    completed_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="bulk_jobs")
    results = db.relationship("BulkPredictionResult", back_populates="job", cascade="all, delete-orphan", lazy="dynamic")

    def to_dict(self):
        return {
            "job_id": self.id,
            "user_id": self.user_id,
            "filename": self.original_filename,
            "status": self.status,
            "total_rows": self.total_rows,
            "valid_rows": self.valid_rows,
            "positive_predictions": self.positive_predictions,
            "negative_predictions": self.negative_predictions,
            "error_message": self.error_message,
            "has_download": bool(self.result_filepath),
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
        }


class BulkPredictionResult(db.Model):
    __tablename__ = "bulk_prediction_results"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    job_id = db.Column(db.String(36), db.ForeignKey("bulk_jobs.id", ondelete="CASCADE"), nullable=False, index=True)

    row_number = db.Column(db.Integer, nullable=False)
    inputs_json = db.Column(db.Text, nullable=False)
    prediction_class = db.Column(db.Integer, nullable=False)
    prediction_label = db.Column(db.String(60), nullable=False)
    probability = db.Column(db.Float, nullable=True)

    job = db.relationship("BulkJob", back_populates="results")

    def get_inputs(self) -> dict:
        try:
            return json.loads(self.inputs_json)
        except (ValueError, TypeError):
            return {}

    def to_dict(self):
        return {
            "row_number": self.row_number,
            "inputs": self.get_inputs(),
            "prediction": self.prediction_class,
            "label": self.prediction_label,
            "probability": self.probability,
        }
