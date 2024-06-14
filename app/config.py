from os import environ


class Config:
    FLASK_ENV = environ.get("FLASK_ENV", "development")
    SECRET_KEY = environ.get("SECRET_KEY", "weretr")
    SQLALCHEMY_DATABASE_URI = environ.get(
        "DATABASE_URL", "postgresql://username:password@localhost/spam_db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = environ.get("JWT_SECRET_KEY", "ergdfb")
    CACHE_TYPE = "redis"
    CACHE_REDIS_HOST = environ.get("CACHE_REDIS_HOST", "localhost")
    CACHE_REDIS_PORT = int(environ.get("CACHE_REDIS_PORT", 6379))
    CACHE_REDIS_DB = int(environ.get("CACHE_REDIS_DB", 0))
    CACHE_REDIS_URL = environ.get("CACHE_REDIS_URL", "redis://localhost:6379/0")
    WTF_CSRF_SECRET_KEY = environ.get("WTF_CSRF_SECRET_KEY", "adsfd")


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False
