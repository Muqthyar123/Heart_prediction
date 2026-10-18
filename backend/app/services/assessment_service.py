from datetime import datetime
from app.extensions import db
from app.models.lifestyle import LifestyleAssessment
from app.models.prediction import HeartPrediction
from app.utils.errors import ForbiddenError, NotFoundError, ValidationError


class AssessmentService:
    @staticmethod
    def get_combined_history(
        user_id: str,
        assessment_type: str = "all",
        page: int = 1,
        per_page: int = 10,
        start_date: str = None,
        end_date: str = None,
    ) -> dict:
        records = []

        if assessment_type in ("all", "heart"):
            query = HeartPrediction.query.filter_by(user_id=user_id)
            if start_date:
                try:
                    dt = datetime.fromisoformat(start_date)
                    query = query.filter(HeartPrediction.created_at >= dt)
                except ValueError:
                    pass
            if end_date:
                try:
                    dt = datetime.fromisoformat(end_date)
                    query = query.filter(HeartPrediction.created_at <= dt)
                except ValueError:
                    pass

            for pred in query.all():
                records.append({
                    "id": pred.id,
                    "type": "heart",
                    "title": f"Heart Disease Prediction ({pred.model_name})",
                    "result_label": pred.prediction_label,
                    "result_code": pred.prediction_code,
                    "probability": pred.probability,
                    "include_in_hospital_summary": pred.include_in_hospital_summary,
                    "created_at": pred.created_at.isoformat(),
                    "details": pred.to_dict(),
                })

        if assessment_type in ("all", "lifestyle"):
            query = LifestyleAssessment.query.filter_by(user_id=user_id)
            if start_date:
                try:
                    dt = datetime.fromisoformat(start_date)
                    query = query.filter(LifestyleAssessment.created_at >= dt)
                except ValueError:
                    pass
            if end_date:
                try:
                    dt = datetime.fromisoformat(end_date)
                    query = query.filter(LifestyleAssessment.created_at <= dt)
                except ValueError:
                    pass

            for life in query.all():
                records.append({
                    "id": life.id,
                    "type": "lifestyle",
                    "title": "Lifestyle Risk Assessment",
                    "result_label": life.category_label,
                    "result_code": life.category_code,
                    "score": life.score,
                    "include_in_hospital_summary": life.include_in_hospital_summary,
                    "created_at": life.created_at.isoformat(),
                    "details": life.to_dict(),
                })

        # Sort descending by created_at
        records.sort(key=lambda x: x["created_at"], reverse=True)

        total = len(records)
        start_idx = (page - 1) * per_page
        end_idx = start_idx + per_page
        paginated_items = records[start_idx:end_idx]

        total_pages = (total + per_page - 1) // per_page if per_page > 0 else 1

        return {
            "items": paginated_items,
            "total": total,
            "page": page,
            "per_page": per_page,
            "pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1,
        }

    @staticmethod
    def get_assessment(assessment_id: str, user_id: str, record_type: str = "heart") -> dict:
        if record_type == "heart":
            rec = db.session.get(HeartPrediction, assessment_id)
        elif record_type == "lifestyle":
            rec = db.session.get(LifestyleAssessment, assessment_id)
        else:
            raise ValidationError("Query param 'type' must be either 'heart' or 'lifestyle'.")

        if not rec:
            raise NotFoundError(f"Assessment '{assessment_id}' not found.")
        if rec.user_id != user_id:
            raise ForbiddenError("You do not have access to this assessment record.")
        return rec.to_dict()

    @staticmethod
    def toggle_hospital_summary_inclusion(assessment_id: str, user_id: str, include: bool) -> dict:
        # Check HeartPrediction first
        pred = db.session.get(HeartPrediction, assessment_id)
        if pred:
            if pred.user_id != user_id:
                raise ForbiddenError("You do not own this prediction record.")
            pred.include_in_hospital_summary = include
            db.session.commit()
            return {"id": pred.id, "type": "heart", "include_in_hospital_summary": pred.include_in_hospital_summary}

        # Check LifestyleAssessment
        life = db.session.get(LifestyleAssessment, assessment_id)
        if life:
            if life.user_id != user_id:
                raise ForbiddenError("You do not own this assessment record.")
            life.include_in_hospital_summary = include
            db.session.commit()
            return {"id": life.id, "type": "lifestyle", "include_in_hospital_summary": life.include_in_hospital_summary}

        raise NotFoundError(f"Assessment record '{assessment_id}' not found.")

    @staticmethod
    def delete_assessment(assessment_id: str, user_id: str):
        pred = db.session.get(HeartPrediction, assessment_id)
        if pred:
            if pred.user_id != user_id:
                raise ForbiddenError("You do not own this prediction record.")
            db.session.delete(pred)
            db.session.commit()
            return

        life = db.session.get(LifestyleAssessment, assessment_id)
        if life:
            if life.user_id != user_id:
                raise ForbiddenError("You do not own this assessment record.")
            db.session.delete(life)
            db.session.commit()
            return

        raise NotFoundError(f"Assessment record '{assessment_id}' not found.")
