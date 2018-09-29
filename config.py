# config.py
import os


class Config():
    """Common configuration class"""
    DEBUG = False
    SECRET_KEY = os.getenv('SECRET_KEY')
    DATABASE_URL = os.getenv('DATABASE_URL')


class Development_config(Config):
    """Configuration for development environment"""

    DEBUG = True


class Testing_config(Config):
    """Configuration for testing environment"""
    TESTING = True
    TEST_DB_URL = os.getenv('TEST_DB_URL')
    DEBUG = True


class Production_config(Config):
    """Configuration for production environment"""
    DEBUG = False


configuration = {
    'development': Development_config,
    'testing': Testing_config,
    'production': Production_config
}
