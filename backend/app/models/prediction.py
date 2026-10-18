import json
import uuid
from datetime import datetime, timezone
from app.extensions import db


class HeartPrediction(db.Model):
    __tablename__ = "heart_predictions"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)
    patient_identifier = db.Column(db.String(60), nullable=True)

    model_name = db.Column(db.String(80), nullable=False, default="hybrid_stacking")
    model_version = db.Column(db.String(30), nullable=False, default="1.0.0")

    # Serialized clinical inputs
    inputs_json = db.Column(db.Text, nullable=False)

    # Prediction outcomes
    prediction_class = db.Column(db.Integer, nullable=False)  # 0 or 1
    prediction_label = db.Column(db.String(60), nullable=False)
    prediction_code = db.Column(db.String(30), nullable=False)  # 'LOWER_RISK' | 'HIGHER_RISK'
    probability = db.Column(db.Float, nullable=True)

    include_in_hospital_summary = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    user = db.relationship("User", back_populates="predictions")

    def get_inputs(self) -> dict:
        try:
            return json.loads(self.inputs_json)
        except (ValueError, TypeError):
            return {}

    def set_inputs(self, data: dict):
        self.inputs_json = json.dumps(data)

    def to_dict(self):
        return {
            "prediction_id": self.id,
            "user_id": self.user_id,
            "patient_identifier": self.patient_identifier,
            "model": self.model_name,
            "model_version": self.model_version,
            "inputs": self.get_inputs(),
            "prediction": {
                "class": self.prediction_class,
                "label": self.prediction_label,
                "code": self.prediction_code,
            },
            "probability": self.probability,
            "include_in_hospital_summary": self.include_in_hospital_summary,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
