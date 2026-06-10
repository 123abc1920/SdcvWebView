from flask import Flask, request, render_template_string
from flask_cors import CORS
from app.shared.extensions import db, migrate
from config import BaseConfig, config_factory
import os
from dotenv import load_dotenv

load_dotenv()


def create_app():
    app = Flask(__name__)
    config_const = os.getenv("CONFIG")
    config = config_factory(config_const)
    app.config.from_object(config)
    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    config.special_init(migrate, app, db)

    from .shared import dbmodels

    return app
