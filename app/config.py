import os
from dataclasses import dataclass, field


def get_database_uri() -> str:
    db_server = os.environ.get("DB_SERVER", "")
    db_name = os.environ.get("DB_NAME", "")
    db_username = os.environ.get("DB_USERNAME", "")
    db_password = os.environ.get("DB_PASSWORD", "")

    if db_server:
        params = "driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
        return f"mssql+pyodbc://{db_username}:{db_password}@{db_server}/{db_name}?{params}"
    return "sqlite:///:memory:"


@dataclass
class Config:
    SECRET_KEY: str = field(default_factory=lambda: os.environ.get("SECRET_KEY", "dev-secret-key"))
    DEBUG: bool = False
    TESTING: bool = False
    SQLALCHEMY_DATABASE_URI: str = field(default_factory=get_database_uri)
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False


@dataclass
class DevelopmentConfig(Config):
    DEBUG: bool = True


@dataclass
class ProductionConfig(Config):
    DEBUG: bool = False


config = {
    "development": DevelopmentConfig,
    "testing": Config,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}
