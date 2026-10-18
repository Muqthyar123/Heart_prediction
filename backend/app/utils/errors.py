import logging
from flask import jsonify, request

logger = logging.getLogger("heartpredict.errors")


class AppError(Exception):
    """Base application exception."""

    status_code = 500
    code = "INTERNAL_SERVER_ERROR"

    def __init__(self, message: str, details=None, status_code=None, code=None):
        super().__init__(message)
        self.message = message
        self.details = details or []
        if status_code is not None:
            self.status_code = status_code
        if code is not None:
            self.code = code


class ValidationError(AppError):
    status_code = 422
    code = "VALIDATION_ERROR"


class BadRequestError(AppError):
    status_code = 400
    code = "BAD_REQUEST"


class UnauthorizedError(AppError):
    status_code = 401
    code = "UNAUTHORIZED"


class ForbiddenError(AppError):
    status_code = 403
    code = "FORBIDDEN"


class NotFoundError(AppError):
    status_code = 404
    code = "NOT_FOUND"


class ConflictError(AppError):
    status_code = 409
    code = "CONFLICT"


class PayloadTooLargeError(AppError):
    status_code = 413
    code = "PAYLOAD_TOO_LARGE"


class UnsupportedMediaTypeError(AppError):
    status_code = 415
    code = "UNSUPPORTED_MEDIA_TYPE"


class RateLimitedError(AppError):
    status_code = 429
    code = "TOO_MANY_REQUESTS"


class ModelUnavailableError(AppError):
    status_code = 503
    code = "MODEL_UNAVAILABLE"


def format_error_response(code: str, message: str, details=None, status_code: int = 400):
    response = {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details or [],
        },
    }
    return jsonify(response), status_code


def register_error_handlers(app):
    """Registers global error handlers conforming to the API specification."""

    @app.errorhandler(AppError)
    def handle_app_error(err):
        return format_error_response(err.code, err.message, err.details, err.status_code)

    @app.errorhandler(400)
    def handle_400(err):
        return format_error_response("BAD_REQUEST", str(getattr(err, "description", "Bad Request")), status_code=400)

    @app.errorhandler(401)
    def handle_401(err):
        return format_error_response("UNAUTHORIZED", "Authentication required.", status_code=401)

    @app.errorhandler(403)
    def handle_403(err):
        return format_error_response("FORBIDDEN", "You do not have permission to perform this action.", status_code=403)

    @app.errorhandler(404)
    def handle_404(err):
        return format_error_response("NOT_FOUND", f"The requested resource was not found: {request.path}", status_code=404)

    @app.errorhandler(405)
    def handle_405(err):
        return format_error_response("METHOD_NOT_ALLOWED", f"The method {request.method} is not allowed for this route.", status_code=405)

    @app.errorhandler(413)
    def handle_413(err):
        return format_error_response("PAYLOAD_TOO_LARGE", "File size exceeds the allowed limit.", status_code=413)

    @app.errorhandler(415)
    def handle_415(err):
        return format_error_response("UNSUPPORTED_MEDIA_TYPE", "Unsupported media type.", status_code=415)

    @app.errorhandler(422)
    def handle_422(err):
        messages = getattr(err, "data", {}).get("messages", ["Unprocessable Entity"])
        return format_error_response("VALIDATION_ERROR", "Validation failed.", details=messages, status_code=422)

    @app.errorhandler(500)
    def handle_500(err):
        logger.error(f"Internal Server Error on {request.path}: {err}", exc_info=True)
        return format_error_response(
            "INTERNAL_SERVER_ERROR",
            "An internal server error occurred. Please try again later.",
            status_code=500,
        )
