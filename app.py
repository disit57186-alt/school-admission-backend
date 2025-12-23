from flask import Flask
from flask_cors import CORS
from config import Config
from extensions import mysql, jwt

from auth.routes import auth_bp
from admissions.routes import admissions_bp
from admin.routes import admin_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)
    mysql.init_app(app)
    jwt.init_app(app)

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(admissions_bp, url_prefix="/api/admissions")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    @app.route("/health")
    def health():
        return {"status": "OK"}

    return app

app = create_app()
