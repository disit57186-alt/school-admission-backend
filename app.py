from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from extensions import mysql, jwt

from auth.routes import auth_bp
from admin.routes import admin_bp
from admissions.routes import admission_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    mysql.init_app(app)
    jwt.init_app(app)

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")
    app.register_blueprint(admission_bp, url_prefix="/api/admissions")

    @app.route("/api/health", methods=["GET"])
    def health():
        return jsonify({
            "status": "OK",
            "message": "Flask API running"
        })

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
