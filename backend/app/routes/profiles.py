from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.schemas.profile_schemas import PatientProfileSchema
from app.services.profile_service import ProfileService
from app.utils.errors import BadRequestError, ValidationError

profiles_bp = Blueprint("profiles", __name__, url_prefix="/api/v1/profiles")
profile_schema = PatientProfileSchema()


@profiles_bp.route("", methods=["POST"])
@jwt_required()
def create_profile():
    user_id = get_jwt_identity()
    json_data = request.get_json(silent=True) or {}
    errors = profile_schema.validate(json_data, partial=True)
    if errors:
        raise ValidationError(message="Validation failed for profile creation.", details=errors)

    profile = ProfileService.update_profile(user_id=user_id, data=json_data, partial=True)
    return jsonify({
        "success": True,
        "data": {
            "profile": profile.to_dict(),
        },
        "meta": {"message": "Profile created successfully."},
    }), 201


@profiles_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_profile():
    user_id = get_jwt_identity()
    profile = ProfileService.get_or_create_profile(user_id)
    return jsonify({
        "success": True,
        "data": {
            "profile": profile.to_dict(),
        },
    })


@profiles_bp.route("/me", methods=["PUT"])
@jwt_required()
def replace_my_profile():
    user_id = get_jwt_identity()
    json_data = request.get_json(silent=True) or {}
    errors = profile_schema.validate(json_data, partial=False)
    if errors:
        raise ValidationError(message="Validation failed for profile replacement.", details=errors)

    profile = ProfileService.update_profile(user_id=user_id, data=json_data, partial=False)
    return jsonify({
        "success": True,
        "data": {
            "profile": profile.to_dict(),
        },
        "meta": {"message": "Profile updated successfully."},
    })


@profiles_bp.route("/me", methods=["PATCH"])
@jwt_required()
def update_my_profile():
    user_id = get_jwt_identity()
    json_data = request.get_json(silent=True) or {}
    errors = profile_schema.validate(json_data, partial=True)
    if errors:
        raise ValidationError(message="Validation failed for profile patch.", details=errors)

    profile = ProfileService.update_profile(user_id=user_id, data=json_data, partial=True)
    return jsonify({
        "success": True,
        "data": {
            "profile": profile.to_dict(),
        },
        "meta": {"message": "Profile updated successfully."},
    })


@profiles_bp.route("/me", methods=["DELETE"])
@jwt_required()
def delete_my_profile():
    user_id = get_jwt_identity()
    ProfileService.delete_profile(user_id)
    return jsonify({
        "success": True,
        "data": {},
        "meta": {"message": "Profile information cleared."},
    })


@profiles_bp.route("/me/photo", methods=["POST"])
@jwt_required()
def upload_profile_photo():
    user_id = get_jwt_identity()
    if "photo" not in request.files:
        raise BadRequestError("No 'photo' file found in request.")

    file_storage = request.files["photo"]
    saved_name = ProfileService.upload_photo(
        user_id=user_id,
        file_storage=file_storage,
        upload_folder=current_app.config["UPLOAD_FOLDER"],
        max_bytes=current_app.config["MAX_CONTENT_LENGTH"],
    )

    return jsonify({
        "success": True,
        "data": {
            "photo_filename": saved_name,
            "photo_url": f"/uploads/profiles/{saved_name}",
        },
        "meta": {"message": "Profile photo uploaded successfully."},
    })


@profiles_bp.route("/me/completion", methods=["GET"])
@jwt_required()
def get_profile_completion():
    user_id = get_jwt_identity()
    completion_data = ProfileService.get_completion_details(user_id)
    return jsonify({
        "success": True,
        "data": completion_data,
    })
