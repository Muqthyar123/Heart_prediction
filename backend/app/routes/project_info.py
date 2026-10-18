from flask import Blueprint, jsonify
from app.extensions import db
from app.services.model_loader import ModelManager
from app.utils.validation import CLINICAL_FEATURE_DEFS

project_info_bp = Blueprint("project_info", __name__, url_prefix="/api/v1")


@project_info_bp.route("/health", methods=["GET"])
def health_check():
    model_mgr = ModelManager.get_instance()

    # Check DB
    db_ok = True
    try:
        db.session.execute(db.text("SELECT 1"))
    except Exception:
        db_ok = False

    status = "healthy" if (model_mgr.is_ready and db_ok) else "degraded"
    status_code = 200 if status == "healthy" else 503

    return jsonify({
        "success": True,
        "data": {
            "status": status,
            "version": "1.0.0",
            "database_connected": db_ok,
            "models_ready": model_mgr.is_ready,
            "models_error": model_mgr.load_error,
            "project_name": "Advanced Heart Disease Prediction System",
            "brand": "HeartPredict AI",
        },
    }), status_code


@project_info_bp.route("/models", methods=["GET"])
def get_models():
    model_mgr = ModelManager.get_instance()
    models_info = model_mgr.get_models_info()
    return jsonify({
        "success": True,
        "data": {
            "models": models_info,
            "total_models": len(models_info),
            "hybrid_architecture": model_mgr.metadata.get(
                "hybrid_architecture",
                "Random Forest + SVM + KNN -> Logistic Regression Meta Learner",
            ),
        },
    })


@project_info_bp.route("/project/info", methods=["GET"])
def get_project_info():
    model_mgr = ModelManager.get_instance()
    return jsonify({
        "success": True,
        "data": {
            "name": "Advanced Heart Disease Prediction System",
            "brand": "HeartPredict AI",
            "version": model_mgr.metadata.get("version", "1.0.0"),
            "description": (
                "An intelligent clinical decision-support system predicting heart disease risk "
                "from 13 clinical biomarkers using an ensemble Hybrid Stacking Classifier."
            ),
            "architecture": {
                "base_models": ["Random Forest", "Support Vector Machine (SVM)", "K-Nearest Neighbors (KNN)"],
                "meta_model": "Logistic Regression",
                "strategy": "5-fold Stratified Stacking Classifier with calibrated probability estimation",
            },
            "preprocessing": model_mgr.metadata.get("preprocessing_pipeline", [
                {"step": "Missing Value Handling", "technique": "Median Imputation"},
                {"step": "Feature Selection", "technique": "RandomForest Feature Importance (Top 10 Biomarkers)"},
                {"step": "Feature Normalization", "technique": "StandardScaler"},
                {"step": "Data Partitioning", "technique": "70% Train, 15% Validation, 15% Test (Stratified)"},
            ]),
            "disclaimer": (
                "This application is intended strictly for research and clinical decision support. "
                "Predictions must be evaluated by licensed medical professionals."
            ),
        },
    })


@project_info_bp.route("/project/features", methods=["GET"])
def get_project_features():
    features_list = []
    for code, info in CLINICAL_FEATURE_DEFS.items():
        item = {
            "code": code,
            "name": info["name"],
            "type": info["type"],
            "description": info["description"],
            "unit": info.get("unit"),
            "min": info.get("min"),
            "max": info.get("max"),
            "options": info.get("options"),
        }
        features_list.append(item)

    return jsonify({
        "success": True,
        "data": {
            "features": features_list,
            "total_features": len(features_list),
            "required_features": list(CLINICAL_FEATURE_DEFS.keys()),
        },
    })


@project_info_bp.route("/project/feature-importance", methods=["GET"])
def get_feature_importance():
    model_mgr = ModelManager.get_instance()
    importances = model_mgr.metadata.get("feature_importances", [])
    return jsonify({
        "success": True,
        "data": {
            "feature_importances": importances,
            "method": "RandomForestClassifier Feature Importance (n_estimators=100)",
            "selected_top_features": model_mgr.get_selected_features(),
        },
    })


@project_info_bp.route("/project/metrics", methods=["GET"])
def get_project_metrics():
    model_mgr = ModelManager.get_instance()
    metrics = model_mgr.metadata.get("model_metrics", {})
    return jsonify({
        "success": True,
        "data": {
            "metrics": metrics,
            "split_ratio": model_mgr.metadata.get("split_ratio", {"train": 0.70, "val": 0.15, "test": 0.15}),
            "verified_from": "Advanced Heart Disease.ipynb test evaluation set",
        },
    })
