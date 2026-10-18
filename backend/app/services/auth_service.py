from datetime import datetime, timezone
from flask_jwt_extended import create_access_token, create_refresh_token
from app.extensions import db
from app.models.profile import PatientProfile
from app.models.token import TokenBlocklist
from app.models.user import User
from app.utils.errors import (
    BadRequestError,
    ConflictError,
    NotFoundError,
    UnauthorizedError,
    ValidationError,
)
from app.utils.security import hash_password, validate_password_strength, verify_password
from app.utils.validation import validate_email_address


class AuthService:
    @staticmethod
    def register(email: str, password: str, full_name: str = None) -> tuple[dict, str, str]:
        email = email.strip().lower()
        if not validate_email_address(email):
            raise ValidationError("Invalid email address format.")

        valid_pw, pw_err = validate_password_strength(password)
        if not valid_pw:
            raise ValidationError(pw_err)

        if User.query.filter_by(email=email).first():
            raise ConflictError("An account with this email address already exists.")

        user = User(
            email=email,
            password_hash=hash_password(password),
            full_name=full_name.strip() if full_name else None,
        )
        db.session.add(user)
        db.session.flush()

        # Initialize blank profile
        profile = PatientProfile(user_id=user.id, full_name=user.full_name)
        db.session.add(profile)
        db.session.commit()

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return user.to_dict(), access_token, refresh_token

    @staticmethod
    def login(email: str, password: str) -> tuple[dict, str, str]:
        email = email.strip().lower()
        user = User.query.filter_by(email=email).first()

        if not user or not verify_password(user.password_hash, password):
            raise UnauthorizedError("Invalid email or password.")

        if not user.is_active:
            raise UnauthorizedError("This account has been deactivated.")

        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return user.to_dict(), access_token, refresh_token

    @staticmethod
    def logout(jwt_payload: dict):
        jti = jwt_payload.get("jti")
        token_type = jwt_payload.get("type", "access")
        user_id = jwt_payload.get("sub")
        exp_timestamp = jwt_payload.get("exp")

        expires_at = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc) if exp_timestamp else None

        revoked_token = TokenBlocklist(
            jti=jti,
            token_type=token_type,
            user_id=user_id,
            expires_at=expires_at,
        )
        db.session.add(revoked_token)
        db.session.commit()

    @staticmethod
    def refresh(user_id: str) -> str:
        user = db.session.get(User, user_id)
        if not user or not user.is_active:
            raise UnauthorizedError("Invalid or inactive user.")
        return create_access_token(identity=user.id)

    @staticmethod
    def change_password(user_id: str, old_password: str, new_password: str):
        user = db.session.get(User, user_id)
        if not user:
            raise NotFoundError("User not found.")

        if not verify_password(user.password_hash, old_password):
            raise UnauthorizedError("Current password is incorrect.")

        valid_pw, pw_err = validate_password_strength(new_password)
        if not valid_pw:
            raise ValidationError(pw_err)

        user.password_hash = hash_password(new_password)
        db.session.commit()
