from . import auth_bp
from .service import auth_service
from flask import request


@auth_bp.route("/login", methods=["POST"])
def login_route():
    """
    Войти в систему
    ---
    tags:
      - features/auth
    responses:
      200:
        description: Успешное получение списка словарей
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: array
                  description: Список названий словарей, доступных в sdcv
                  items:
                    type: string
                  example: ["Mueller7GPL", "Full English-Russian", "LingvoUniversal"]
      500:
        description: Внутренняя ошибка сервера при обращении к контейнеру sdcv
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Failed to fetch dictionaries from container"
    """
    result = {}

    if result["success"] == True:
        return {"data": result["data"]}, 200
    else:
        return {"message": result["data"]}, 409


@auth_bp.route("/signup", methods=["POST"])
def signup_route():
    """
    Зарегистрироваться в системе
    ---
    tags:
      - features/auth
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - user_name
              - password
            properties:
              user_name:
                type: string
                description: Имя пользователя
                example: "Test User"
              password:
                type: string
                description: Пароль
                example: "123456"
    responses:
      200:
        description: Успешное создание
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: str
                  description: JWT токен
                  example: "5r67gthu99ojjiijji"
      409:
        description: Внутренняя ошибка сервера при обращении к контейнеру sdcv
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Failed to fetch dictionaries from container"
    """
    data = request.get_json()

    user_name = data.get("user_name")
    password = data.get("password")

    result = auth_service.signup(user_name, password)

    if result["success"] == True:
        return {"data": result["data"]}, 200
    else:
        return {"message": result["data"]}, 409


@auth_bp.route("/get/data", methods=["GET"])
def get_data_route():
    """
    Получить данные аккаунта
    ---
    tags:
      - features/auth
    responses:
      200:
        description: Успешное получение списка словарей
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: array
                  description: Список названий словарей, доступных в sdcv
                  items:
                    type: string
                  example: ["Mueller7GPL", "Full English-Russian", "LingvoUniversal"]
      500:
        description: Внутренняя ошибка сервера при обращении к контейнеру sdcv
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Failed to fetch dictionaries from container"
    """
    result = {}

    if result["success"] == True:
        return {"data": result["data"]}, 200
    else:
        return {"message": result["data"]}, 409


@auth_bp.route("/delete/user", methods=["DELETE"])
def delete_user_route():
    """
    Удалить пользователя
    ---
    tags:
      - features/auth
    responses:
      200:
        description: Успешное получение списка словарей
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: array
                  description: Список названий словарей, доступных в sdcv
                  items:
                    type: string
                  example: ["Mueller7GPL", "Full English-Russian", "LingvoUniversal"]
      500:
        description: Внутренняя ошибка сервера при обращении к контейнеру sdcv
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Failed to fetch dictionaries from container"
    """
    result = {}

    if result["success"] == True:
        return {"data": result["data"]}, 200
    else:
        return {"message": result["data"]}, 409
