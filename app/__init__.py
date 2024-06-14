from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from flask_caching import Cache
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
import os

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
bcrypt = Bcrypt()
cache = Cache(config={"CACHE_TYPE": "redis"})
csrf = CSRFProtect()
limiter = Limiter(
    get_remote_address,
    storage_uri="redis://localhost:6379",
    storage_options={"socket_connect_timeout": 30},
    strategy="fixed-window",
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(
        "app.config.DevelopmentConfig"
        if os.environ.get("FLASK_ENV") == "development"
        else "app.config.DevelopmentConfig"
    )

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cache.init_app(app)

    if app.config["FLASK_ENV"] == "production":
        csrf.init_app(app)
        limiter.init_app(app)
        CORS(
            app,
            resources={r"*": {"origins": "https://instahyre_coding_task.onrender.com"}},
        )
    else:
        CORS(app, resources={r"*": {"origins": "*"}})

    from app import routes, auth

    app.register_blueprint(routes.bp)
    app.register_blueprint(auth.bp)

    @app.after_request
    def apply_caching(response):
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "SAMEORIGIN"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        return response

    return app
