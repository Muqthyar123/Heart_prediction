import os
import uuid
from werkzeug.utils import secure_filename
from app.utils.errors import BadRequestError, PayloadTooLargeError, UnsupportedMediaTypeError


def get_file_extension(filename: str) -> str:
    """Returns lowercased extension without the dot."""
    if "." in filename:
        return filename.rsplit(".", 1)[1].lower()
    return ""


def is_allowed_file(filename: str, allowed_extensions: set[str]) -> bool:
    ext = get_file_extension(filename)
    return ext in allowed_extensions


def save_secure_file(
    file_storage,
    target_dir: str,
    allowed_extensions: set[str],
    max_bytes: int = 16 * 1024 * 1024,
) -> tuple[str, str, int]:
    """
    Saves an uploaded file safely:
    - Verifies extension
    - Generates a UUID filename to prevent collisions and path traversal
    - Verifies file size
    Returns (saved_filename, full_path, file_size_bytes).
    """
    if not file_storage or not file_storage.filename:
        raise BadRequestError("No file provided.")

    original_name = file_storage.filename
    ext = get_file_extension(original_name)
    if not ext or ext not in allowed_extensions:
        raise UnsupportedMediaTypeError(
            f"Unsupported file type .{ext}. Allowed types: {', '.join(sorted(allowed_extensions))}"
        )

    # Secure the directory
    os.makedirs(target_dir, exist_ok=True)

    # Generate unique filename
    unique_name = f"{uuid.uuid4().hex}.{ext}"
    destination_path = os.path.join(target_dir, unique_name)

    # Verify no path traversal
    if not os.path.abspath(destination_path).startswith(os.path.abspath(target_dir)):
        raise BadRequestError("Invalid file path.")

    file_storage.save(destination_path)
    file_size = os.path.getsize(destination_path)

    if file_size > max_bytes:
        try:
            os.remove(destination_path)
        except OSError:
            pass
        raise PayloadTooLargeError(f"File size ({file_size} bytes) exceeds limit of {max_bytes} bytes.")

    return unique_name, destination_path, file_size
