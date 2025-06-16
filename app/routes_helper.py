# routes_helper.py
import os
from flask import current_app, flash
from werkzeug.utils import secure_filename
from app.services import assign_user_type

def handle_profile_image_upload(file, user):
    if not file:
        return

    filename = secure_filename(file.filename)
    uploads_dir = current_app.config['UPLOAD_FOLDER']
    os.makedirs(uploads_dir, exist_ok=True)
    file_path = os.path.join(uploads_dir, filename)

    if os.path.isdir(file_path):
        flash("Upload error: The destination path is a directory, not a file.", "danger")
        return False

    ext = os.path.splitext(filename.lower())[1]
    if ext not in [".jpg", ".jpeg", ".png"]:
        error_msg = f"Invalid image format: {ext}. Only JPEG and PNG are supported."
        flash("Invalid image format. Only JPEG and PNG are supported.", "danger")
        current_app.logger.error(error_msg)
        return False

    file.save(file_path)
    user.profile_image = filename
    return True

def update_user_typology(user, typology_name, type_value):
    """Backward-compatible wrapper around :func:`assign_user_type`."""
    assign_user_type(user, typology_name, type_value)
