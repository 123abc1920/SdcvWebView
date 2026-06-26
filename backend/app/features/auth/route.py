from . import auth_bp
from .service import auth_service
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_pydantic import validate
from .requests import LoginRequest
from .responses import JWTResponse


@auth_bp.route("/login", methods=["POST"])
@validate()
def login_route(body: LoginRequest):
    """
    Войти в систему и получить JWT токен
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
        description: Успешная авторизация
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
                  type: string
                  description: JWT токен доступа (Access Token)
                  example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                error:
                  type: string
                  nullable: true
                  example: null
      400:
        description: Ошибка валидации (не переданы обязательные поля)
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
                            example: "Test User"
                          loc:
                            type: array
                            items:
                              type: string
                            example: ["password"]
                          msg:
                            type: string
                            example: "Field required"
                          type:
                            type: string
                            example: "missing"
      409:
        description: Ошибка авторизации (неверный логин или пароль)
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
                  example: "Invalid username or password"
    """
    user_name = body.user_name
    password = body.password

    result = auth_service.login(user_name, password)

    if result["success"] == True:
        return JWTResponse(success=True, data=result["data"]), 200
    else:
        return JWTResponse(success=False, error=result["data"]), 409


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
@jwt_required()
def get_data_route():
    """
    Получить данные аккаунта
    ---
    tags:
      - features/auth
    security:
      - BearerAuth: []
    definitions:
      securitySchemes:
        BearerAuth:
          type: apiKey
          name: Authorization
          in: header
    responses:
      200:
        description: Успешное получение данных пользователя
        content:
          application/json:
            schema:
              type: object
              properties:
                data:
                  type: object
                  properties:
                    user_name:
                      type: string
                      description: Имя пользователя
                      example: "admin"
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
        description: Конфликт (логическая ошибка, например, пользователь не найден)
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "User not found"
    """
    user_id = get_jwt_identity()

    result = auth_service.get_user_data(user_id)

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

    result = auth_service.delete(user_name, password)

    if result["success"] == True:
        return {"data": result["data"]}, 200
    else:
        return {"message": result["data"]}, 409
