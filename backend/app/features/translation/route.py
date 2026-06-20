from . import translation_bp
from flask import request
from .service import translate_service

SDCV_TEST_CONTAINER = "sdcv-test"


@translation_bp.route("/translate", methods=["GET"])
def translate():
    word = request.args.get("word")

    result = translate_service.translate(SDCV_TEST_CONTAINER, word)
    print(*result)

    return "test", 200
