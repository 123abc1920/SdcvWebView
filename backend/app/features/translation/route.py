from . import translation_bp
from flask import request
from .service import translate_service
from flask_jwt_extended import jwt_required, get_jwt_identity

SDCV_TEST_CONTAINER = "sdcv-test"


@translation_bp.route("/translate", methods=["POST"])
@jwt_required(optional=True)
def translate():
    """
    Перевод слова через sdcv
    ---
    tags:
      - features/translation
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - word
            properties:
              word:
                type: string
                description: Слово для перевода
                example: "meet"
              filters:
                type: array
                description: Список словарей для фильтрации
                items:
                  type: string
                example: ["Mueller7GPL", "Full English-Russian"]
    responses:
      200:
        description: Успешный перевод
        content:
          application/json:
            schema:
              type: object
              properties:
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
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Word not found"
    """
    data = request.get_json()

    word = data.get("word")
    filters = data.get("filters", [])

    result = translate_service.translate(SDCV_TEST_CONTAINER, word, filters)

    user_id = get_jwt_identity()
    if user_id:
        save_history_res = translate_service.save_history(word, user_id)

    if result["success"] == True:
        return {"data": result["data"]}, 200
    else:
        return {"message": result["data"]}, 409
