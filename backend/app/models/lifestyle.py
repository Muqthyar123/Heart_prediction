import json
import uuid
from datetime import datetime, timezone
from app.extensions import db


class LifestyleAssessment(db.Model):
    __tablename__ = "lifestyle_assessments"

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = db.Column(db.String(36), db.ForeignKey("users.id", ondelete="CASCADE"), nullable=True, index=True)

    answers_json = db.Column(db.Text, nullable=False)
    score = db.Column(db.Float, nullable=False)  # 0 to 100
    category = db.Column(db.String(30), nullable=False)  # 'lower' | 'moderate' | 'higher'
    category_label = db.Column(db.String(60), nullable=False)
    category_code = db.Column(db.String(30), nullable=False)

    breakdown_json = db.Column(db.Text, nullable=False)
    recommendations_json = db.Column(db.Text, nullable=False)

    include_in_hospital_summary = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False, index=True)

    user = db.relationship("User", back_populates="lifestyle_assessments")

    def get_answers(self) -> dict:
        try:
            return json.loads(self.answers_json)
        except (ValueError, TypeError):
            return {}

    def get_breakdown(self) -> list:
        try:
            return json.loads(self.breakdown_json)
        except (ValueError, TypeError):
            return []

    def get_recommendations(self) -> list:
        try:
            return json.loads(self.recommendations_json)
        except (ValueError, TypeError):
            return []

    def to_dict(self):
        return {
            "assessment_id": self.id,
            "user_id": self.user_id,
            "score": self.score,
            "category": self.category,
            "category_label": self.category_label,
            "category_code": self.category_code,
            "breakdown": self.get_breakdown(),
            "recommendations": self.get_recommendations(),
            "answers": self.get_answers(),
            "include_in_hospital_summary": self.include_in_hospital_summary,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
