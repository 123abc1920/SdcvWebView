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
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "SQLALCHEMY_DATABASE_URI_TEST", "sqlite:///test.db"
    )
    CONFIG: str = "DEBUG"
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "3xvX3jfKiSOoFFGVcIM5Hkd9o")
    APP_NAME: str = os.getenv("APP_NAME", "SDCV API")
    OPEN_API_V: str = os.getenv("OPEN_API_V", "3.0.2")

    def special_init(self, migrate, app, db):
        app.config["JWT_SECRET_KEY"] = self.JWT_SECRET_KEY
        app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(
            days=JWT_ACCESS_TOKEN_EXPIRES
        )


class DebugConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "SQLALCHEMY_DATABASE_URI_TEST", "sqlite:///test.db"
    )
    CONFIG: str = "DEBUG"

    def special_init(self, migrate, app, db):
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

        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
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
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "SQLALCHEMY_DATABASE_URI_PROD", "sqlite:///app.db"
    )
    CONFIG: str = "PRODUCT"

    def special_init(self, migrate, app, db):
        pass


configs = [DebugConfig(), ProductConfig()]


def config_factory(config: str) -> BaseConfig:
    for c in configs:
        if config == c.CONFIG:
            return c

    return configs[0]
