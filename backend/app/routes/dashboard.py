from flask import Blueprint, jsonify
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.models.lifestyle import LifestyleAssessment
from app.models.prediction import HeartPrediction
from app.services.assessment_service import AssessmentService
from app.services.profile_service import ProfileService
from app.utils.i18n import get_current_language, get_text

dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api/v1/dashboard")


@dashboard_bp.route("/summary", methods=["GET"])
@jwt_required()
def get_dashboard_summary():
    user_id = get_jwt_identity()
    lang = get_current_language()

    # Profile completion
    comp = ProfileService.get_completion_details(user_id)

    # Latest Heart Prediction
    latest_heart = (
        HeartPrediction.query.filter_by(user_id=user_id)
        .order_by(HeartPrediction.created_at.desc())
        .first()
    )

    # Latest Lifestyle Assessment
    latest_lifestyle = (
        LifestyleAssessment.query.filter_by(user_id=user_id)
        .order_by(LifestyleAssessment.created_at.desc())
        .first()
    )

    # Total counts
    total_heart = HeartPrediction.query.filter_by(user_id=user_id).count()
    total_lifestyle = LifestyleAssessment.query.filter_by(user_id=user_id).count()

    reminders = []
    if not comp["is_complete"]:
        reminders.append({
            "code": "PROFILE_INCOMPLETE",
            "message": get_text("profile_incomplete_reminder", lang),
            "missing_sections": comp["missing_sections"],
        })

    return jsonify({
        "success": True,
        "data": {
            "profile_completion": comp["completion_percentage"],
            "profile_is_complete": comp["is_complete"],
            "total_heart_assessments": total_heart,
            "total_lifestyle_assessments": total_lifestyle,
            "latest_heart_assessment": latest_heart.to_dict() if latest_heart else None,
            "latest_lifestyle_assessment": latest_lifestyle.to_dict() if latest_lifestyle else None,
            "reminders": reminders,
        },
    })


@dashboard_bp.route("/recent-activity", methods=["GET"])
@jwt_required()
def get_recent_activity():
    user_id = get_jwt_identity()
    history = AssessmentService.get_combined_history(user_id=user_id, page=1, per_page=5)
    return jsonify({
        "success": True,
        "data": {
            "recent_activity": history["items"],
        },
    })
