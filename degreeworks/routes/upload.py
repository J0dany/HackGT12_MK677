import os
import shutil
from flask import Blueprint, request, jsonify
from routes.parser import parse_degreeworks_remaining

upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/upload", methods=["POST"])
def upload_degreeworks():
    # Ensure uploads folder exists
    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    # Check if file was uploaded
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Save file to uploads/
    file_path = os.path.join("uploads", file.filename)
    file.save(file_path)

    # Parse DegreeWorks PDF
    remaining_courses = parse_degreeworks_remaining(file_path)

    if not remaining_courses:
        return jsonify({"error": "Could not detect remaining courses in the PDF"}), 400

    return jsonify({"remaining_courses": remaining_courses})
