import os
from flask import Flask, jsonify
from app.config import config_by_name
from app.extensions import cors, db, jwt, migrate
from app.routes import (
    assessments_bp,
    auth_bp,
    bulk_bp,
    dashboard_bp,
    hospital_summary_bp,
    lifestyle_bp,
    predictions_bp,
    profiles_bp,
    project_info_bp,
)
from app.services.model_loader import ModelManager
from app.utils.errors import register_error_handlers
from app.utils.security import init_jwt_callbacks


def create_app(config_name: str = None) -> Flask:
    if config_name is None:
        config_name = os.getenv("FLASK_ENV", "development")

    app = Flask(__name__)
    cfg = config_by_name.get(config_name, config_by_name["default"])
    app.config.from_object(cfg)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(
        app,
        resources={r"/api/*": {"origins": app.config.get("CORS_ORIGINS", "*")}},
        supports_credentials=True,
    )

    # Initialize JWT Callbacks
    with app.app_context():
        init_jwt_callbacks()

    # Register Error Handlers
    register_error_handlers(app)

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(profiles_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(predictions_bp)
    app.register_blueprint(bulk_bp)
    app.register_blueprint(lifestyle_bp)
    app.register_blueprint(assessments_bp)
    app.register_blueprint(hospital_summary_bp)
    app.register_blueprint(project_info_bp)

    # Initialize Machine Learning Artifacts
    artifacts_dir = app.config.get("ARTIFACTS_DIR")
    if artifacts_dir:
        ModelManager.get_instance().initialize(artifacts_dir)

    # Ensure Upload Directories Exist
    upload_folder = app.config.get("UPLOAD_FOLDER")
    if upload_folder:
        os.makedirs(os.path.join(upload_folder, "profiles"), exist_ok=True)
        os.makedirs(os.path.join(upload_folder, "bulk"), exist_ok=True)

    @app.route("/", methods=["GET"])
    def root():
        return jsonify({
            "name": "HeartPredict AI Backend API",
            "version": "1.0.0",
            "status": "online",
            "docs": "/api/v1/project/info",
            "health": "/api/v1/health",
        })

    return app
