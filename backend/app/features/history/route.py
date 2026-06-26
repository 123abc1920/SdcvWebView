from . import history_bp
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .service import history_service
from flask_pydantic import validate
from .validation import HistoryResponseSchema
from app.shared.validation import ApiResponse


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
              properties:
                data:
                  type: array
                  items:
                    type: object
                    properties:
                      id:
                        type: integer
                        example: 7
                      word:
                        type: string
                        example: "meet"
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
        description: Ошибка сервера
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Database error"
    """
    user_id = get_jwt_identity()

    result = history_service.get_history(user_id)

    if result["success"]:
        return (
            HistoryResponseSchema(success=True, data=result["data"]),
            200,
        )
    else:
        return (
            HistoryResponseSchema(success=False, error=result["data"]),
            409,
        )


@history_bp.route("/delete/history", methods=["DELETE"])
@jwt_required()
@validate()
def delete_history_item():
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
        description: Ошибка сервера
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Database error"
    """
    user_id = get_jwt_identity()

    data = request.get_json()
    ids = data.get("ids", [])

    result = history_service.delete_history(ids, user_id)

    if result["success"]:
        return (
            ApiResponse(success=True, data=result["data"]),
            200,
        )
    else:
        return (
            ApiResponse(success=False, error=result["data"]),
            409,
        )
