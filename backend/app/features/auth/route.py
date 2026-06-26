from . import auth_bp
from .service import auth_service
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_pydantic import validate
from .requests import AuthRequest
from .responses import JWTResponse, UserDataResponse, DeleteResponse


@auth_bp.route("/login", methods=["POST"])
@validate()
def login_route(body: AuthRequest):
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
@validate()
def signup_route(body: AuthRequest):
    """
    Зарегистрироваться в системе и получить JWT токен
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
        description: Успешная регистрация и создание пользователя
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
        description: Ошибка валидации (не переданы обязательные поля или пустые строки)
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
                            example: ["user_name"]
                          msg:
                            type: string
                            example: "String should have at least 1 character"
                          type:
                            type: string
                            example: "string_too_short"
      409:
        description: Ошибка регистрации (пользователь уже существует / ошибка БД)
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
                  example: "Username already exists"
    """
    user_name = body.user_name
    password = body.password

    result = auth_service.signup(user_name, password)

    if result["success"] == True:
        return JWTResponse(success=True, data=result["data"]), 200
    else:
        return JWTResponse(success=False, error=result["data"]), 409


@auth_bp.route("/get/data", methods=["GET"])
@jwt_required()
@validate()
def get_data_route():
    """
    Получить данные аккаунта
    ---
    tags:
      - features/auth
    security:
      - BearerAuth: []
    responses:
      200:
        description: Успешное получение данных пользователя
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
                  required: [user_name]
                  properties:
                    user_name:
                      type: string
                      description: Имя пользователя
                      example: "admin"
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
        description: Конфликт (логическая ошибка, например, пользователь не найден)
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
                  example: "User not found"
    """
    user_id = get_jwt_identity()

    result = auth_service.get_user_data(user_id)

    if result["success"]:
        return UserDataResponse(success=True, data=result["data"]), 200
    else:
        return UserDataResponse(success=False, error=result["data"]), 409


@auth_bp.route("/delete/user", methods=["DELETE"])
@validate()
def delete_user_route(body: AuthRequest):
    """
    Удалить аккаунт пользователя из системы
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
        description: Аккаунт пользователя успешно удален
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
        description: Ошибка валидации входящих учетных данных (Pydantic)
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
                            example: ["password"]
                          msg:
                            type: string
                            example: "Field required"
                          type:
                            type: string
                            example: "missing"
      409:
        description: Ошибка удаления (неверный пароль или пользователь не найден)
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
                  example: "Invalid password or user does not exist"
    """
    user_name = body.user_name
    password = body.password

    result = auth_service.delete(user_name, password)

    if result["success"]:
        return DeleteResponse(success=True, data=result["data"]), 200
    else:
        return DeleteResponse(success=False, error=result["data"]), 409
