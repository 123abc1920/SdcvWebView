import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from flasgger import Swagger

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
        pass


class DebugConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "SQLALCHEMY_DATABASE_URI_TEST", "sqlite:///test.db"
    )
    CONFIG: str = "DEBUG"

    def special_init(self, migrate, app, db):
        migrate.init_app(app, db)

        app.config["SWAGGER"] = {
            "title": self.APP_NAME,
            "openapi": self.OPEN_API_V,
            "specs_route": "/apidocs/",
        }
        swagger = Swagger(app)

        print("Swagger on localhost:5200/apidocs")


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
