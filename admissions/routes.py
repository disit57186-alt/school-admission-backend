from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import mysql
import hashlib

admissions_bp = Blueprint("admissions", __name__)

@admissions_bp.route("/submit", methods=["POST"])
@jwt_required()
def submit_admission():
    user_id = get_jwt_identity()
    data = request.json

    duplicate_hash = hashlib.sha256(
        f"{data['parent_mobile']}{data['latitude']}".encode()
    ).hexdigest()

    cur = mysql.connection.cursor()

    cur.execute(
        "SELECT id FROM admissions WHERE duplicate_check_hash=%s",
        (duplicate_hash,)
    )
    if cur.fetchone():
        return jsonify({"error": "Duplicate lead"}), 409

    cur.execute("""
        INSERT INTO admissions
        (user_id, student_name, admission_class,
         parent_mobile, latitude, longitude,
         gps_accuracy, is_mock_location,
         image_url, image_hash, duplicate_check_hash)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        user_id,
        data["student_name"],
        data["admission_class"],
        data["parent_mobile"],
        data["latitude"],
        data["longitude"],
        data["gps_accuracy"],
        data["is_mock_location"],
        data["image_url"],
        data["image_hash"],
        duplicate_hash
    ))

    mysql.connection.commit()
    return jsonify({"message": "Lead submitted"}), 201
