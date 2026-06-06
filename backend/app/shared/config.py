import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class BaseConfig(BaseSettings):
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "SQLALCHEMY_DATABASE_URI_TEST", "sqlite:///test.db"
    )
    CONFIG: str = "DEBUG"

    def special_init(self, migrate, app, db):
        pass


class DebugConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "SQLALCHEMY_DATABASE_URI_TEST", "sqlite:///test.db"
    )
    CONFIG: str = "DEBUG"

    def special_init(self, migrate, app, db):
        migrate.init_app(app, db)


class ProductConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI: str = os.getenv(
        "SQLALCHEMY_DATABASE_URI_PROD", "sqlite:///test.db"
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
