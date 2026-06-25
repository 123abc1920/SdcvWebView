from flask import Flask, request, render_template_string
from flask_cors import CORS
from app.shared.extensions import db, migrate, main_config
from config import config_factory
import os
from dotenv import load_dotenv
from app.features import translation_bp, dicts_bp, auth_bp, history_bp
from flask_jwt_extended import JWTManager

load_dotenv()


def create_app():
    app = Flask(__name__)
    config_const = os.getenv("CONFIG")
    config = config_factory(config_const)
    app.config.from_object(config)
    CORS(app, resources={r"/*": {"origins": "*"}})

    jwt = JWTManager(app)

    global main_config
    main_config = config

    app.register_blueprint(translation_bp)
    app.register_blueprint(dicts_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(history_bp)

    db.init_app(app)
    config.special_init(migrate, app, db)

    from .shared import dbmodels

    return app
