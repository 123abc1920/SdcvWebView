from . import translation_bp
from .service import translate_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_pydantic import validate
from .requests import TranslateRequest
from .responses import TranslateResponseSchema
from app.shared.dto import BaseDTO

SDCV_TEST_CONTAINER = "sdcv-test"


@translation_bp.route("/translate", methods=["POST"])
@jwt_required(optional=True)
@validate()
def translate(body: TranslateRequest):
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
              required: [data, error]
              properties:
                data:
                  type: array
                  items:
                    type: object
                    required: [dict, definition]
                    properties:
                      dict:
                        type: string
                        example: "Mueller7GPL"
                      definition:
                        type: string
                        example: "встречать"
                error:
                  type: string
                  nullable: true
                  example: null
      400:
        description: Ошибка валидации входящего JSON (Pydantic)
        content:
          application/json:
            schema:
              type: object
              properties:
                validation_error:
                  type: object
                  properties:
                    body_params:
                      type: array
                      items:
                        type: object
                        properties:
                          input:
                            type: string
                            example: ""
                          loc:
                            type: array
                            items:
                              type: string
                            example: ["word"]
                          msg:
                            type: string
                            example: "Field required"
                          type:
                            type: string
                            example: "missing"
      409:
        description: Ошибка перевода
        content:
          application/json:
            schema:
              type: object
              required: [data, error]
              properties:
                data:
                  type: object
                  nullable: true
                  example: null
                error:
                  type: string
                  example: "Word not found"
    """
    word = body.word

    result = translate_service.translate(SDCV_TEST_CONTAINER, word, body.filters)

    user_id = get_jwt_identity()
    if user_id:
        save_history_res = translate_service.save_history(word, user_id)

    if result.error:
        return TranslateResponseSchema(error=result.error), 409
    else:
        return TranslateResponseSchema(data=result.data), 200
