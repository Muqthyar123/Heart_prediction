from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.assessment_service import AssessmentService
from app.utils.errors import BadRequestError

assessments_bp = Blueprint("assessments", __name__, url_prefix="/api/v1/assessments")


@assessments_bp.route("/history", methods=["GET"])
@jwt_required()
def get_combined_history():
    user_id = get_jwt_identity()
    assessment_type = request.args.get("type", "all").lower()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")

    result = AssessmentService.get_combined_history(
        user_id=user_id,
        assessment_type=assessment_type,
        page=page,
        per_page=per_page,
        start_date=start_date,
        end_date=end_date,
    )
    return jsonify({
        "success": True,
        "data": result,
    })


@assessments_bp.route("/<assessment_id>", methods=["GET"])
@jwt_required()
def get_assessment_detail(assessment_id: str):
    user_id = get_jwt_identity()
    rec_type = request.args.get("type", "heart").lower()
    data = AssessmentService.get_assessment(assessment_id, user_id=user_id, record_type=rec_type)
    return jsonify({
        "success": True,
        "data": data,
    })


@assessments_bp.route("/<assessment_id>/hospital-summary", methods=["PATCH"])
@jwt_required()
def toggle_hospital_summary(assessment_id: str):
    user_id = get_jwt_identity()
    json_data = request.get_json(silent=True) or {}
    if "include_in_hospital_summary" not in json_data:
        raise BadRequestError("Key 'include_in_hospital_summary' (boolean) is required.")

    include = bool(json_data["include_in_hospital_summary"])
    updated = AssessmentService.toggle_hospital_summary_inclusion(
        assessment_id=assessment_id, user_id=user_id, include=include
    )
    return jsonify({
        "success": True,
        "data": updated,
        "meta": {"message": "Hospital summary inclusion preference updated."},
    })


@assessments_bp.route("/<assessment_id>", methods=["DELETE"])
@jwt_required()
def delete_assessment_record(assessment_id: str):
    user_id = get_jwt_identity()
    AssessmentService.delete_assessment(assessment_id=assessment_id, user_id=user_id)
    return jsonify({
        "success": True,
        "data": {},
        "meta": {"message": "Assessment record deleted."},
    })
