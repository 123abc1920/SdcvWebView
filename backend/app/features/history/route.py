from . import history_bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from .service import history_service
from flask_pydantic import validate
from .requests import DeleteHistoryRequestSchema
from .responses import HistoryResponseSchema
from app.shared.validation import ApiResponse
from app.shared.dto import BaseDTO


@history_bp.route("/history", methods=["GET"])
@jwt_required()
@validate()
def get_history_route():
    """
    Получение истории пользователя
    ---
    tags:
      - features/history
    security:
      - BearerAuth: []
    responses:
      200:
        description: Успешное получение истории
        content:
          application/json:
            schema:
              type: object
              required: [success, data, error]
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: array
                  items:
                    type: object
                    required: [id, word]
                    properties:
                      id:
                        type: integer
                        example: 7
                      word:
                        type: string
                        example: "meet"
                error:
                  type: string
                  nullable: true
                  example: null
      401:
        description: Не авторизован (отсутствует или невалидный JWT)
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Missing Authorization Header"
      409:
        description: Ошибка сервера / Бизнес-ошибка
        content:
          application/json:
            schema:
              type: object
              required: [success, data, error]
              properties:
                success:
                  type: boolean
                  example: false
                data:
                  type: object
                  nullable: true
                  example: null
                error:
                  type: string
                  example: "Database error"
    """
    user_id = get_jwt_identity()

    result = history_service.get_history(user_id)

    if result.error:
        return (
            HistoryResponseSchema(success=False, error=result.error),
            409,
        )
    else:
        return (
            HistoryResponseSchema(success=True, data=result.data),
            200,
        )


@history_bp.route("/delete/history", methods=["DELETE"])
@jwt_required()
@validate()
def delete_history_item(body: DeleteHistoryRequestSchema):
    """
    Удаляет записи в истории пользователя
    ---
    tags:
      - features/history
    security:
      - BearerAuth: []
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required: [ids]
            properties:
              ids:
                type: array
                description: Id для удаления
                items:
                  type: integer
                example: [7, 8, 3]
    responses:
      200:
        description: Успешное удаление
        content:
          application/json:
            schema:
              type: object
              required: [success, data, error]
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: object
                  nullable: true
                  example: null
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
                            example: "jhgjk"
                          loc:
                            type: array
                            items:
                              type: string
                            example: ["ids", 0]
                          msg:
                            type: string
                            example: "Input should be a valid integer..."
                          type:
                            type: string
                            example: "int_parsing"
                          url:
                            type: string
                            example: "https://pydantic.dev..."
      401:
        description: Не авторизован (отсутствует или невалидный JWT)
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Missing Authorization Header"
      409:
        description: Ошибка сервера / Бизнес-ошибка
        content:
          application/json:
            schema:
              type: object
              required: [success, data, error]
              properties:
                success:
                  type: boolean
                  example: false
                data:
                  type: object
                  nullable: true
                  example: null
                error:
                  type: string
                  example: "Database error"
    """
    user_id = get_jwt_identity()

    result = history_service.delete_history(body.ids, user_id)

    if result.error:
        return (
            ApiResponse(success=False, error=result.error),
            409,
        )
    else:
        return (
            ApiResponse(success=True, data=result.data),
            200,
        )
