from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.schemas.lifestyle_schemas import LifestyleInputSchema
from app.services.lifestyle_service import LifestyleService
from app.utils.errors import ValidationError
from app.utils.i18n import get_current_language

lifestyle_bp = Blueprint("lifestyle", __name__, url_prefix="/api/v1/lifestyle-assessments")
lifestyle_schema = LifestyleInputSchema()


@lifestyle_bp.route("", methods=["POST"])
@jwt_required(optional=True)
def submit_lifestyle_assessment():
    user_id = get_jwt_identity()
    json_data = request.get_json(silent=True) or {}
    lang = get_current_language()

    errors = lifestyle_schema.validate(json_data)
    if errors:
        raise ValidationError(message="Validation failed for lifestyle inputs.", details=errors)

    save_to_history = json_data.get("save_to_history", True)
    answers = {k: json_data[k] for k in ["activity", "diet", "smoking", "alcohol", "sleep", "stress", "weight"]}

    result = LifestyleService.create_assessment(
        answers=answers,
        user_id=user_id,
        save_to_history=save_to_history,
        lang=lang,
    )

    return jsonify({
        "success": True,
        "data": result,
    }), 201


@lifestyle_bp.route("/history", methods=["GET"])
@jwt_required()
def get_lifestyle_history():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    history = LifestyleService.get_user_history(user_id=user_id, page=page, per_page=per_page)
    return jsonify({
        "success": True,
        "data": history,
    })


@lifestyle_bp.route("/<assessment_id>", methods=["GET"])
@jwt_required(optional=True)
def get_lifestyle_assessment(assessment_id: str):
    user_id = get_jwt_identity()
    assessment = LifestyleService.get_assessment_by_id(assessment_id, user_id=user_id)
    return jsonify({
        "success": True,
        "data": assessment,
    })


@lifestyle_bp.route("/<assessment_id>", methods=["DELETE"])
@jwt_required()
def delete_lifestyle_assessment(assessment_id: str):
    user_id = get_jwt_identity()
    LifestyleService.delete_assessment(assessment_id, user_id=user_id)
    return jsonify({
        "success": True,
        "data": {},
        "meta": {"message": "Lifestyle assessment deleted."},
    })
