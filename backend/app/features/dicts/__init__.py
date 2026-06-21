from flask import Blueprint

dicts_bp = Blueprint("dicts", __name__)
from . import route
