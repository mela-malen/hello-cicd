import os
import logging
from flask import Flask
from .config import config
from .data.models import db
from sqlalchemy import text

logger = logging.getLogger(__name__)


def create_app(config_name: str | None = None) -> Flask:
    if config_name is None:
        config_name = os.environ.get("FLASK_ENV", "development")

    app = Flask(
        __name__,
        template_folder="presentation/templates",
        static_folder="presentation/static",
    )

    app.config.from_object(config[config_name]())

    db.init_app(app)

    with app.app_context():
        try:
            db.create_all()
            logger.info("Database tables created successfully")
            
            # Run migration to add missing columns
            _run_migration()
            
            # Ensure admin user exists
            _ensure_admin_user()
        except Exception as e:
            logger.warning(f"Could not create database tables (may need migration): {e}")

    from .presentation.routes.public import bp as public_bp
    app.register_blueprint(public_bp)

    from app.presentation.routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    return app


def _run_migration():
    """Run database migration to add missing columns."""
    try:
        result = db.session.execute(text("""
            SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE TABLE_NAME = 'subscribers'
            ORDER BY ORDINAL_POSITION
        """))
        columns = [row[0] for row in result]
        
        for col in ['nl_kost', 'nl_mindset', 'nl_kunskap', 'nl_veckans_pass', 'nl_jaine']:
            if col not in columns:
                logger.info(f"Adding missing column: {col}")
                try:
                    db.session.execute(text(f'ALTER TABLE subscribers ADD {col} BIT NOT NULL DEFAULT 0'))
                    db.session.commit()
                    logger.info(f"Successfully added column: {col}")
                except Exception as e:
                    db.session.rollback()
                    logger.warning(f"Failed to add column {col}: {e}")
    except Exception as e:
        logger.warning(f"Migration check failed: {e}")


def _ensure_admin_user():
    """Ensure default admin user exists."""
    from .data.models import User
    
    admin_username = os.environ.get("ADMIN_USERNAME", "admin")
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin123")
    
    try:
        existing_user = User.query.filter_by(username=admin_username).first()
        if not existing_user:
            admin_user = User(username=admin_username)
            admin_user.set_password(admin_password)
            db.session.add(admin_user)
            db.session.commit()
            logger.info(f"Created default admin user: {admin_username}")
        else:
            logger.info(f"Admin user already exists: {admin_username}")
    except Exception as e:
        db.session.rollback()
        logger.warning(f"Could not create admin user: {e}")
