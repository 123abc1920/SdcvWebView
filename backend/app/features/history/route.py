from . import history_bp
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from .service import history_service


@history_bp.route("/history", methods=["GET"])
@jwt_required()
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

    if result["success"] == True:
        return {"data": result["data"]}, 200
    else:
        return {"message": result["data"]}, 409
