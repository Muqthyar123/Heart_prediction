from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from app.schemas.auth_schemas import ChangePasswordSchema, LoginSchema, RegisterSchema
from app.services.auth_service import AuthService
from app.utils.errors import ValidationError

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/auth")
register_schema = RegisterSchema()
login_schema = LoginSchema()
change_pw_schema = ChangePasswordSchema()


@auth_bp.route("/register", methods=["POST"])
def register():
    json_data = request.get_json(silent=True) or {}
    errors = register_schema.validate(json_data)
    if errors:
        raise ValidationError(message="Validation failed for registration.", details=errors)

    user_dict, access_token, refresh_token = AuthService.register(
        email=json_data["email"],
        password=json_data["password"],
        full_name=json_data.get("full_name"),
    )

    return (
        jsonify({
            "success": True,
            "data": {
                "user": user_dict,
                "access_token": access_token,
                "refresh_token": refresh_token,
            },
            "meta": {"message": "Account created successfully."},
        }),
        201,
    )


@auth_bp.route("/login", methods=["POST"])
def login():
    json_data = request.get_json(silent=True) or {}
    errors = login_schema.validate(json_data)
    if errors:
        raise ValidationError(message="Validation failed for login.", details=errors)

    user_dict, access_token, refresh_token = AuthService.login(
        email=json_data["email"],
        password=json_data["password"],
    )

    return jsonify({
        "success": True,
        "data": {
            "user": user_dict,
            "access_token": access_token,
            "refresh_token": refresh_token,
        },
        "meta": {"message": "Login successful."},
    })


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    payload = get_jwt()
    AuthService.logout(payload)
    return jsonify({
        "success": True,
        "data": {},
        "meta": {"message": "Successfully logged out. Token revoked."},
    })


@auth_bp.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    from app.extensions import db
    from app.models.user import User

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({"success": False, "error": {"code": "NOT_FOUND", "message": "User not found."}}), 404

    return jsonify({
        "success": True,
        "data": {
            "user": user.to_dict(),
        },
    })


@auth_bp.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh_token():
    user_id = get_jwt_identity()
    new_access_token = AuthService.refresh(user_id)
    return jsonify({
        "success": True,
        "data": {
            "access_token": new_access_token,
        },
        "meta": {"message": "Access token refreshed."},
    })


@auth_bp.route("/change-password", methods=["POST"])
@jwt_required()
def change_password():
    user_id = get_jwt_identity()
    json_data = request.get_json(silent=True) or {}
    errors = change_pw_schema.validate(json_data)
    if errors:
        raise ValidationError(message="Validation failed.", details=errors)

    AuthService.change_password(
        user_id=user_id,
        old_password=json_data["old_password"],
        new_password=json_data["new_password"],
    )

    return jsonify({
        "success": True,
        "data": {},
        "meta": {"message": "Password changed successfully."},
    })
