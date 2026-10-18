from app.routes.assessments import assessments_bp
from app.routes.auth import auth_bp
from app.routes.bulk import bulk_bp
from app.routes.dashboard import dashboard_bp
from app.routes.hospital_summary import hospital_summary_bp
from app.routes.lifestyle import lifestyle_bp
from app.routes.predictions import predictions_bp
from app.routes.profiles import profiles_bp
from app.routes.project_info import project_info_bp

__all__ = [
    "auth_bp",
    "profiles_bp",
    "dashboard_bp",
    "predictions_bp",
    "bulk_bp",
    "lifestyle_bp",
    "assessments_bp",
    "hospital_summary_bp",
    "project_info_bp",
]
