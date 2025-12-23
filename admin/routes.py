from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from extensions import mysql

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/users/pending")
@jwt_required()
def pending_users():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM users WHERE status='PENDING'")
    return jsonify(cur.fetchall())


@admin_bp.route("/users/approve", methods=["POST"])
@jwt_required()
def approve_user():
    user_id = request.json["user_id"]
    cur = mysql.connection.cursor()

    cur.execute("""
        UPDATE users
        SET status='APPROVED', approved_at=NOW()
        WHERE id=%s
    """, (user_id,))
    mysql.connection.commit()

    return jsonify({"message": "User approved"})

@admin_bp.route("/analytics/day-wise")
@jwt_required()
def day_wise():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT DATE(created_at) AS day, COUNT(*) total
        FROM admissions
        GROUP BY DATE(created_at)
        ORDER BY day DESC
    """)
    return jsonify(cur.fetchall())


@admin_bp.route("/analytics/month-wise")
@jwt_required()
def month_wise():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT YEAR(created_at) year, MONTH(created_at) month, COUNT(*) total
        FROM admissions
        GROUP BY year, month
        ORDER BY year DESC, month DESC
    """)
    return jsonify(cur.fetchall())

