import os
import logging
from flask import Flask
from .config import config
from .data.models import db

logger = logging.getLogger(__name__)


def create_app(config_name: str | None = None) -> Flask:
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(
        __name__,
        template_folder="presentation/templates",
        static_folder="presentation/static",
    )

    # Load configuration (instantiate dataclass)
    app.config.from_object(config[config_name]())

    # Initialize database
    db.init_app(app)

    # Try to create tables, but don't fail if connection fails
    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.warning(f"Could not create database tables (may need migration): {e}")

    # Register blueprints
    from .presentation.routes.public import bp as public_bp
    app.register_blueprint(public_bp)

    from app.presentation.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    return app
