from flask import Flask, request, render_template_string
from flask_cors import CORS
from app.shared.extensions import db, migrate
from config import BaseConfig


def app_factory(config: BaseConfig):
    app = Flask(__name__)
    app.config.from_object(config)
    CORS(app, resources={r"/*": {"origins": "*"}})

    db.init_app(app)
    config.special_init(migrate, app, db)

    return app
