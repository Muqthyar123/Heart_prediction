from app.extensions import db
from app.models.prediction import HeartPrediction
from app.services.model_loader import ModelManager
from app.utils.errors import ForbiddenError, NotFoundError, ValidationError
from app.utils.i18n import get_text
from app.utils.validation import validate_clinical_inputs


class PredictionService:
    @staticmethod
    def predict_heart_disease(
        features: dict,
        model_name: str = "hybrid_stacking",
        user_id: str = None,
        save_to_history: bool = True,
        patient_identifier: str = None,
        lang: str = "en",
    ) -> dict:
        cleaned_features, errors = validate_clinical_inputs(features)
        if errors:
            raise ValidationError(
                message="Clinical input validation failed.",
                details=errors,
            )

        model_mgr = ModelManager.get_instance()
        pred_result = model_mgr.predict(cleaned_features, model_name=model_name)

        label_key = "higher_risk_label" if pred_result["prediction_class"] == 1 else "lower_risk_label"
        desc_key = "higher_risk_desc" if pred_result["prediction_class"] == 1 else "lower_risk_desc"

        localized_label = get_text(label_key, lang)
        localized_desc = get_text(desc_key, lang)
        disclaimer = get_text("disclaimer", lang)

        prediction_record = None
        if user_id and save_to_history:
            prediction_record = HeartPrediction(
                user_id=user_id,
                patient_identifier=patient_identifier,
                model_name=pred_result["model_name"],
                model_version=pred_result["model_version"],
                prediction_class=pred_result["prediction_class"],
                prediction_label=pred_result["prediction_label"],
                prediction_code=pred_result["prediction_code"],
                probability=pred_result["probability"],
            )
            prediction_record.set_inputs(cleaned_features)
            db.session.add(prediction_record)
            db.session.commit()

        pred_id = prediction_record.id if prediction_record else "ephemeral-prediction"

        return {
            "prediction_id": pred_id,
            "model": pred_result["model_name"],
            "model_version": pred_result["model_version"],
            "prediction": {
                "class": pred_result["prediction_class"],
                "label": localized_label,
                "code": pred_result["prediction_code"],
                "description": localized_desc,
            },
            "probability": pred_result["probability"],
            "inputs": cleaned_features,
            "disclaimer": disclaimer,
            "saved_to_history": bool(prediction_record),
            "created_at": prediction_record.created_at.isoformat() if prediction_record else None,
        }

    @staticmethod
    def get_prediction_by_id(prediction_id: str, user_id: str = None) -> dict:
        pred = db.session.get(HeartPrediction, prediction_id)
        if not pred:
            raise NotFoundError(f"Prediction record '{prediction_id}' not found.")
        if user_id and pred.user_id != user_id:
            raise ForbiddenError("You do not have permission to view this prediction record.")
        return pred.to_dict()

    @staticmethod
    def delete_prediction(prediction_id: str, user_id: str):
        pred = db.session.get(HeartPrediction, prediction_id)
        if not pred:
            raise NotFoundError(f"Prediction record '{prediction_id}' not found.")
        if pred.user_id != user_id:
            raise ForbiddenError("You do not have permission to delete this prediction record.")
        db.session.delete(pred)
        db.session.commit()

    @staticmethod
    def get_user_prediction_history(user_id: str, page: int = 1, per_page: int = 10) -> dict:
        pagination = (
            HeartPrediction.query.filter_by(user_id=user_id)
            .order_by(HeartPrediction.created_at.desc())
            .paginate(page=page, per_page=per_page, error_out=False)
        )
        return {
            "items": [item.to_dict() for item in pagination.items],
            "total": pagination.total,
            "pages": pagination.pages,
            "page": pagination.page,
            "per_page": pagination.per_page,
            "has_next": pagination.has_next,
            "has_prev": pagination.has_prev,
        }
