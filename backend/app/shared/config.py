import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from flasgger import Swagger
import logging
from logging.handlers import RotatingFileHandler
from datetime import timedelta
from app.shared.consts import JWT_ACCESS_TOKEN_EXPIRES

load_dotenv()


class BaseConfig(BaseSettings):
    """
    Base configuration class managing core application environment settings.
    """

    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "SQLALCHEMY_DATABASE_URI_TEST", "sqlite:///app.db"
    )
    """The database connection URI string."""
    CONFIG: str = "DEBUG"
    """The configuration environment identifier string."""
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "3xvX3jfKiSOoFFGVcIM5Hkd9o")
    """The secret key used for signing JWT access tokens."""
    APP_NAME: str = os.getenv("APP_NAME", "SDCV API")
    """The application name used across metadata and interfaces."""
    OPEN_API_V: str = os.getenv("OPEN_API_V", "3.0.2")
    """The target OpenAPI specification version version string."""

    def special_init(self, migrate, app, db):
        """
        Initializes core base application components and JWT configurations.

        Args:
            migrate: The Flask-Migrate extension instance.
            app: The current Flask application instance.
            db: The SQLAlchemy database instance.
        """
        app.config["JWT_SECRET_KEY"] = self.JWT_SECRET_KEY
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
            days=JWT_ACCESS_TOKEN_EXPIRES
        )


class DebugConfig(BaseConfig):
    """
    Development configuration environment containing Swagger documentation and extended logging.
    """

    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "SQLALCHEMY_DATABASE_URI_TEST", "sqlite:///app.db"
    )
    """The database connection URI string used for debugging/testing."""
    CONFIG: str = "DEBUG"
    """The configuration environment identifier string set to debug mode."""

    def special_init(self, migrate, app, db):
        """
        Sets up the application in debug mode, initializing Swagger UI and active logging structures.

        Args:
            migrate: The Flask-Migrate extension instance.
            app: The current Flask application instance.
            db: The SQLAlchemy database instance.
        """
        super().special_init(migrate, app, db)

        migrate.init_app(app, db)

        app.config["SWAGGER"] = {
            "title": self.APP_NAME,
            "openapi": self.OPEN_API_V,
            "specs_route": "/apidocs/",
        }
        swagger_template = {
            "openapi": self.OPEN_API_V,
            "info": {"title": self.APP_NAME, "version": "1.0.0"},
            "components": {
                "securitySchemes": {
                    "BearerAuth": {
                        "type": "http",
                        "scheme": "bearer",
                        "bearerFormat": "JWT",
                    }
                }
            },
        }
        swagger = Swagger(app, template=swagger_template)

        print("Swagger on localhost:5200/apidocs")

        CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
        BASE_DIR = os.path.dirname(CURRENT_DIR)
        BASE_DIR = os.path.dirname(BASE_DIR)
        logging.basicConfig(
            level=logging.DEBUG,
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            handlers=[
                RotatingFileHandler(
                    os.path.join(BASE_DIR, "logs", "logs.log"),
                    encoding="utf-8",
                    maxBytes=10_000_000,
                    backupCount=5,
                ),
                logging.StreamHandler(),
            ],
        )

        print("Logs on backend/logs/")


class ProductConfig(BaseConfig):
    """
    Production configuration environment optimized for stable system deployment.
    """

    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "SQLALCHEMY_DATABASE_URI_PROD", "sqlite:///app.db"
    )
    """The live production database connection URI string."""
    CONFIG: str = "PRODUCT"
    """The configuration environment identifier string set to production mode."""

    def special_init(self, migrate, app, db):
        """
        Executes production-specific initialization logic.

        Args:
            migrate: The Flask-Migrate extension instance.
            app: The current Flask application instance.
            db: The SQLAlchemy database instance.
        """
        pass


configs = [DebugConfig(), ProductConfig()]
"""A list of initialized configuration options available to the factory method."""


def config_factory(config: str) -> BaseConfig:
    """
    Factory function matching a runtime configuration identifier string against active environments.

    Args:
        config (str): The configuration environment code identifier (e.g. 'DEBUG', 'PRODUCT').

    Returns:
        BaseConfig: A configuration subclass matching the specified identifier, defaulting to debug mode if unmatched.
    """
    for c in configs:
        if config == c.CONFIG:
            return c

    return configs[0]
