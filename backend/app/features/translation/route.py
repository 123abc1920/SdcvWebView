from . import translation_bp
from flask import request
from .service import translate_service

SDCV_TEST_CONTAINER = "sdcv-test"


@translation_bp.route("/translate", methods=["GET"])
def translate():
    """
    Перевод слова через sdcv
    ---
    tags:
      - features/translation
    parameters:
      - name: word
        in: query
        type: string
        required: true
        description: Слово для перевода
        example: "meet"
    responses:
      200:
        description: Успешный перевод
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: true
            data:
              type: array
              items:
                type: object
                properties:
                  dict_name:
                    type: string
                    example: "Mueller7GPL"
                  content:
                    type: string
                    example: "встречать"
      409:
        description: Ошибка перевода
        schema:
          type: object
          properties:
            success:
              type: boolean
              example: false
            error:
              type: string
              example: "Word not found"
    """
    word = request.args.get("word")

    result = translate_service.translate(SDCV_TEST_CONTAINER, word)

    print(result)

    if result["success"]:
        return result["data"], 200
    else:
        return result["data"], 409
