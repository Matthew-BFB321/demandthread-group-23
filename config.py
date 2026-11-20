"""Settings for each environments. APP_ENV in .env chooses one."""
import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-me")
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = False  #users get a JSON error message

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
class ProductionConfig(Config):
    pass

CONFIGS = {"development": DevelopmentConfig,
           "testing": TestingConfig,
           "production": ProductionConfig}