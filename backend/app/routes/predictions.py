from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.schemas.prediction_schemas import SinglePredictionRequestSchema
from app.services.model_loader import ModelManager
from app.services.prediction_service import PredictionService
from app.utils.errors import ValidationError
from app.utils.i18n import get_current_language

predictions_bp = Blueprint("predictions", __name__, url_prefix="/api/v1/predictions")
single_pred_schema = SinglePredictionRequestSchema()


@predictions_bp.route("/heart", methods=["POST"])
@jwt_required(optional=True)
def predict_heart():
    user_id = get_jwt_identity()
    json_data = request.get_json(silent=True) or {}
    lang = get_current_language()

    # Support both { features: { ... } } or direct { age: ..., sex: ... }
    if "features" in json_data and isinstance(json_data["features"], dict):
        features = json_data["features"]
        model_name = json_data.get("model_name", "hybrid_stacking")
        save_to_history = json_data.get("save_to_history", True)
        patient_id = json_data.get("patient_identifier")
    else:
        features = json_data
        model_name = json_data.get("model_name", "hybrid_stacking")
        save_to_history = json_data.get("save_to_history", True)
        patient_id = json_data.get("patient_identifier")

    result = PredictionService.predict_heart_disease(
        features=features,
        model_name=model_name,
        user_id=user_id,
        save_to_history=save_to_history,
        patient_identifier=patient_id,
        lang=lang,
    )

    return jsonify({
        "success": True,
        "data": result,
    }), 201 if result.get("saved_to_history") else 200


@predictions_bp.route("/models", methods=["GET"])
def get_available_models():
    model_mgr = ModelManager.get_instance()
    models_info = model_mgr.get_models_info()
    return jsonify({
        "success": True,
        "data": {
            "models": models_info,
            "default_model": "hybrid_stacking",
            "is_ready": model_mgr.is_ready,
        },
    })


@predictions_bp.route("/history", methods=["GET"])
@jwt_required()
def get_prediction_history():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    history = PredictionService.get_user_prediction_history(
        user_id=user_id, page=page, per_page=per_page
    )
    return jsonify({
        "success": True,
        "data": history,
    })


@predictions_bp.route("/<prediction_id>", methods=["GET"])
@jwt_required(optional=True)
def get_single_prediction(prediction_id: str):
    user_id = get_jwt_identity()
    pred = PredictionService.get_prediction_by_id(prediction_id, user_id=user_id)
    return jsonify({
        "success": True,
        "data": pred,
    })


@predictions_bp.route("/<prediction_id>", methods=["DELETE"])
@jwt_required()
def delete_single_prediction(prediction_id: str):
    user_id = get_jwt_identity()
    PredictionService.delete_prediction(prediction_id, user_id=user_id)
    return jsonify({
        "success": True,
        "data": {},
        "meta": {"message": "Prediction record deleted."},
    })
