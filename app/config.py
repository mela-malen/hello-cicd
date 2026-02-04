import os
from dataclasses import dataclass


@dataclass
class Config:
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "dev-secret-key")
    DEBUG: bool = False
    TESTING: bool = False


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
