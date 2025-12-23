from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from extensions import mysql
import bcrypt

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    cur = mysql.connection.cursor()

    password_hash = bcrypt.hashpw(
        data["password"].encode(), bcrypt.gensalt()
    ).decode()

    cur.execute("""
        INSERT INTO users
        (name, mobile, email, password_hash,
         device_id, device_model, os_version, app_version)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        data["name"],
        data["mobile"],
        data.get("email"),
        password_hash,
        data["device_id"],
        data["device_model"],
        data["os_version"],
        data["app_version"]
    ))

    mysql.connection.commit()
    return jsonify({"message": "Registered. Await admin approval"}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    cur = mysql.connection.cursor()

    cur.execute("SELECT * FROM users WHERE mobile=%s", (data["mobile"],))
    user = cur.fetchone()

    if not user or user["status"] != "APPROVED":
        return jsonify({"error": "Not approved"}), 403

    if not bcrypt.checkpw(
        data["password"].encode(),
        user["password_hash"].encode()
    ):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=user["id"])

    cur.execute(
        "UPDATE users SET last_login=NOW() WHERE id=%s",
        (user["id"],)
    )
    mysql.connection.commit()

    return jsonify(access_token=token)
