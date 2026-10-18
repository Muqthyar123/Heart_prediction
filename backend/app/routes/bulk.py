import os
from flask import Blueprint, current_app, jsonify, request, send_file
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.services.bulk_prediction_service import BulkPredictionService
from app.utils.errors import BadRequestError, NotFoundError

bulk_bp = Blueprint("bulk", __name__, url_prefix="/api/v1/bulk")


@bulk_bp.route("/validate", methods=["POST"])
def validate_bulk_file():
    if "file" not in request.files:
        raise BadRequestError("No file uploaded. Key 'file' is required.")

    file_storage = request.files["file"]
    upload_folder = current_app.config["UPLOAD_FOLDER"]
    temp_dir = os.path.join(upload_folder, "bulk", "temp")
    os.makedirs(temp_dir, exist_ok=True)

    from app.utils.file_handling import save_secure_file

    saved_name, full_path, _ = save_secure_file(
        file_storage,
        target_dir=temp_dir,
        allowed_extensions={"csv", "xlsx", "xls"},
        max_bytes=current_app.config["MAX_CONTENT_LENGTH"],
    )

    try:
        df = BulkPredictionService.read_spreadsheet(full_path)
        summary = BulkPredictionService.validate_file_content(
            df, max_rows=current_app.config["MAX_BULK_ROWS"]
        )
    finally:
        # Clean up temporary file
        try:
            os.remove(full_path)
        except OSError:
            pass

    return jsonify({
        "success": True,
        "data": summary,
    })


@bulk_bp.route("/predict", methods=["POST"])
@jwt_required(optional=True)
def run_bulk_prediction():
    user_id = get_jwt_identity()
    if "file" not in request.files:
        raise BadRequestError("No file uploaded. Key 'file' is required.")

    file_storage = request.files["file"]
    model_name = request.form.get("model_name", "hybrid_stacking")

    result = BulkPredictionService.process_bulk_prediction(
        file_storage=file_storage,
        upload_folder=current_app.config["UPLOAD_FOLDER"],
        user_id=user_id,
        max_rows=current_app.config["MAX_BULK_ROWS"],
        sync_limit=current_app.config["SYNCHRONOUS_BULK_LIMIT"],
        model_name=model_name,
    )

    return jsonify({
        "success": True,
        "data": result,
    }), 201


@bulk_bp.route("/jobs/<job_id>", methods=["GET"])
@jwt_required(optional=True)
def get_job_status(job_id: str):
    user_id = get_jwt_identity()
    job = BulkPredictionService.get_job_by_id(job_id, user_id=user_id)
    return jsonify({
        "success": True,
        "data": job.to_dict(),
    })


@bulk_bp.route("/jobs/<job_id>/results", methods=["GET"])
@jwt_required(optional=True)
def get_job_results(job_id: str):
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 50, type=int)

    results_data = BulkPredictionService.get_job_results_paginated(
        job_id=job_id, user_id=user_id, page=page, per_page=per_page
    )
    return jsonify({
        "success": True,
        "data": results_data,
    })


@bulk_bp.route("/jobs/<job_id>/download", methods=["GET"])
@jwt_required(optional=True)
def download_job_results(job_id: str):
    user_id = get_jwt_identity()
    job = BulkPredictionService.get_job_by_id(job_id, user_id=user_id)

    if not job.result_filepath or not os.path.exists(job.result_filepath):
        raise NotFoundError("Result file not found or expired.")

    download_name = f"HeartPredict_Results_{job.original_filename.rsplit('.', 1)[0]}.xlsx"
    return send_file(
        job.result_filepath,
        as_attachment=True,
        download_name=download_name,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@bulk_bp.route("/template", methods=["GET"])
def download_template():
    stream = BulkPredictionService.generate_excel_template()
    return send_file(
        stream,
        as_attachment=True,
        download_name="HeartPredict_Patient_Template.xlsx",
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
