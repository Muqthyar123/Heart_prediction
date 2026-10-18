import re
from werkzeug.security import check_password_hash, generate_password_hash
from app.extensions import jwt


def hash_password(password: str) -> str:
    """Hashes a password securely using Werkzeug's default method."""
    return generate_password_hash(password)


def verify_password(stored_hash: str, password: str) -> bool:
    """Verifies a password against its stored hash."""
    if not stored_hash or not password:
        return False
    return check_password_hash(stored_hash, password)


def validate_password_strength(password: str) -> tuple[bool, str]:
    """Ensures password satisfies security criteria."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters long."
    if not re.search(r"\d", password):
        return False, "Password must contain at least one digit."
    if not re.search(r"[a-zA-Z]", password):
        return False, "Password must contain at least one letter."
    return True, ""


def init_jwt_callbacks():
    """Initializes Flask-JWT-Extended blocklist and user lookup callbacks."""
    from app.models.token import TokenBlocklist
    from app.models.user import User

    @jwt.token_in_blocklist_loader
    def check_if_token_revoked(jwt_header, jwt_payload: dict) -> bool:
        jti = jwt_payload.get("jti")
        if not jti:
            return False
        token = TokenBlocklist.query.filter_by(jti=jti).first()
        return token is not None

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data) -> User | None:
        identity = jwt_data.get("sub")
        if identity is None:
            return None
        from app.extensions import db
        return db.session.get(User, identity)
