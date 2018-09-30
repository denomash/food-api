# config.py


class Config():
    """Common configuration class"""
    DEBUG = False


class Development_config(Config):
    """Configuration for development environment"""

    DEBUG = True


class Testing_config(Config):
    """Configuration for testing environment"""
    TESTING = True
    DATABASE_URL = 'dbname=test_db user=test password=test host=localhost'
    DEBUG = True


class Production_config(Config):
    """Configuration for production environment"""
    DEBUG = False


configuration = {
    'development': Development_config,
    'testing': Testing_config,
    'production': Production_config
}
