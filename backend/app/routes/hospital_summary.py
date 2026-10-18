import io
from flask import Blueprint, Response, jsonify, request, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.schemas.summary_schemas import ShareSummarySchema, SummaryPreferenceSchema
from app.services.hospital_summary_service import HospitalSummaryService
from app.utils.errors import ValidationError
from app.utils.i18n import get_current_language

hospital_summary_bp = Blueprint("hospital_summary", __name__, url_prefix="/api/v1/hospital-summary")
share_schema = ShareSummarySchema()
pref_schema = SummaryPreferenceSchema()


@hospital_summary_bp.route("", methods=["GET"])
@jwt_required()
def get_summary():
    user_id = get_jwt_identity()
    lang = get_current_language()
    data = HospitalSummaryService.get_summary_data(user_id=user_id, lang=lang)
    return jsonify({
        "success": True,
        "data": data,
    })


@hospital_summary_bp.route("/preview", methods=["GET"])
@jwt_required()
def preview_summary_html():
    user_id = get_jwt_identity()
    lang = get_current_language()
    html_content = HospitalSummaryService.generate_html_summary(user_id=user_id, lang=lang)
    return Response(html_content, mimetype="text/html")


@hospital_summary_bp.route("/download", methods=["GET"])
@jwt_required()
def download_summary():
    user_id = get_jwt_identity()
    lang = get_current_language()
    html_content = HospitalSummaryService.generate_html_summary(user_id=user_id, lang=lang)

    stream = io.BytesIO(html_content.encode("utf-8"))
    return send_file(
        stream,
        as_attachment=True,
        download_name="HeartPredict_Clinical_Summary.html",
        mimetype="text/html",
    )


@hospital_summary_bp.route("/share", methods=["POST"])
@jwt_required()
def share_summary():
    user_id = get_jwt_identity()
    json_data = request.get_json(silent=True) or {}
    errors = share_schema.validate(json_data)
    if errors:
        raise ValidationError(message="Validation failed for sharing consent.", details=errors)

    ip_addr = request.remote_addr
    user_agent = request.headers.get("User-Agent")

    result = HospitalSummaryService.share_summary(
        user_id=user_id,
        data=json_data,
        ip_address=ip_addr,
        user_agent=user_agent,
    )
    return jsonify({
        "success": True,
        "data": result,
        "meta": {"message": "Consent recorded and clinical summary prepared."},
    })


@hospital_summary_bp.route("/preferences", methods=["PUT", "PATCH"])
@jwt_required()
def update_preferences():
    user_id = get_jwt_identity()
    json_data = request.get_json(silent=True) or {}
    errors = pref_schema.validate(json_data, partial=True)
    if errors:
        raise ValidationError(message="Validation failed for preferences.", details=errors)

    pref = HospitalSummaryService.update_preferences(user_id=user_id, data=json_data)
    return jsonify({
        "success": True,
        "data": {
            "preferences": pref.to_dict(),
        },
        "meta": {"message": "Hospital summary preferences updated."},
    })
