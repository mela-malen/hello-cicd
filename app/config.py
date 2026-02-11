import os
from dataclasses import dataclass


@dataclass
class Config:
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key")
    DEBUG: bool = False
    TESTING: bool = False

    # Database configuration
    DB_SERVER: str = os.environ.get("DB_SERVER", "")
    DB_NAME: str = os.environ.get("DB_NAME", "")
    DB_USERNAME: str = os.environ.get("DB_USERNAME", "")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.DB_SERVER:
            params = "driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
            return f"mssql+pyodbc://{self.DB_USERNAME}:{self.DB_PASSWORD}@{self.DB_SERVER}/{self.DB_NAME}?{params}"
        return "sqlite:///:memory:"

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
