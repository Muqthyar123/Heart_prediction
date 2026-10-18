import os
from datetime import timedelta
from dotenv import load_dotenv

# Load .env file from backend root if present
basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
load_dotenv(os.path.join(basedir, ".env"))


class Config:
    """Base configuration with safe defaults."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-heartpredict-ai-2026")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-key-heartpredict-ai-2026")

    # Token Lifetimes
    access_minutes = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", 30))
    refresh_days = int(os.getenv("JWT_REFRESH_TOKEN_EXPIRES_DAYS", 30))
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=access_minutes)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=refresh_days)
    JWT_BLOCKLIST_ENABLED = True
    JWT_BLOCKLIST_TOKEN_CHECKS = ["access", "refresh"]

    # SQLAlchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL", f"sqlite:///{os.path.join(basedir, 'heartpredict.db')}"
    )

    # CORS
    cors_env = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173,http://localhost:4173,http://localhost:8080",
    )
    CORS_ORIGINS = [origin.strip() for origin in cors_env.split(",") if origin.strip()]

    # File Uploads
    UPLOAD_FOLDER = os.path.join(basedir, os.getenv("UPLOAD_FOLDER", "uploads"))
    MAX_CONTENT_LENGTH = int(os.getenv("MAX_CONTENT_LENGTH_MB", 16)) * 1024 * 1024
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    ALLOWED_BULK_EXTENSIONS = {"csv", "xlsx", "xls"}

    # Bulk processing limits
    MAX_BULK_ROWS = int(os.getenv("MAX_BULK_ROWS", 5000))
    SYNCHRONOUS_BULK_LIMIT = int(os.getenv("SYNCHRONOUS_BULK_LIMIT", 500))

    # Artifacts
    ARTIFACTS_DIR = os.getenv("ARTIFACTS_DIR", os.path.join(basedir, "artifacts"))
    if not os.path.isabs(ARTIFACTS_DIR):
        ARTIFACTS_DIR = os.path.join(basedir, ARTIFACTS_DIR)

    # Security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"


class DevelopmentConfig(Config):
    DEBUG = True
    ENV = "development"


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=5)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=1)
    WTF_CSRF_ENABLED = False


class ProductionConfig(Config):
    DEBUG = False
    ENV = "production"
    # Ensure strong secrets in production
    SESSION_COOKIE_SECURE = True


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
