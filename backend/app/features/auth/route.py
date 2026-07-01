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
    Log in to the system and receive a JWT token
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
                description: The user's name
                example: "Test User"
              password:
                type: string
                description: Password
                example: "123456"
    responses:
      200:
        description: Successful authorization
        content:
          application/json:
            schema:
              type: object
              required: [data, error]
              properties:
                data:
                  type: string
                  description: JWT access token (Access Token)
                  example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                error:
                  type: string
                  nullable: true
                  example: null
      400:
        description: Validation error (required fields are missing)
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
        description: Authorization error (invalid username or password)
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
                  example: "Invalid username or password"
    """
    user_name = body.user_name
    password = body.password

    result = auth_service.login(user_name, password)

    if result.error:
        return JWTResponse(error=result.error), 409
    else:
        return JWTResponse(data=result.data), 200


@auth_bp.route("/signup", methods=["POST"])
@validate()
def signup_route(body: AuthRequest):
    """
    Register in the system and receive a JWT token
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
                description: The user's name
                example: "Test User"
              password:
                type: string
                description: Password
                example: "123456"
    responses:
      200:
        description: Successful registration and user creation
        content:
          application/json:
            schema:
              type: object
              required: [data, error]
              properties:
                data:
                  type: string
                  description: JWT access token (Access Token)
                  example: "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
                error:
                  type: string
                  nullable: true
                  example: null
      400:
        description: Validation error (required fields are missing or empty strings)
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
        description: Registration error (user already exists / database error)
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
                  example: "Username already exists"
    """
    user_name = body.user_name
    password = body.password

    result = auth_service.signup(user_name, password)

    if result.error:
        return JWTResponse(error=result.error), 409
    else:
        return JWTResponse(data=result.data), 200


@auth_bp.route("/get/data", methods=["GET"])
@jwt_required()
@validate()
def get_data_route():
    """
    Get account data
    ---
    tags:
      - features/auth
    security:
      - BearerAuth: []
    responses:
      200:
        description: Successful retrieval of user data
        content:
          application/json:
            schema:
              type: object
              required: [data, error]
              properties:
                data:
                  type: object
                  required: [user_name]
                  properties:
                    user_name:
                      type: string
                      description: The user's name
                      example: "admin"
                error:
                  type: string
                  nullable: true
                  example: null
      401:
        description: Unauthorized (missing or invalid JWT)
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Missing Authorization Header"
      409:
        description: Conflict (logical error, for example, user not found)
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
                  example: "User not found"
    """
    user_id = get_jwt_identity()

    result = auth_service.get_user_data(user_id)

    if result.error:
        return UserDataResponse(error=result.error), 409
    else:
        return UserDataResponse(data=result.data), 200


@auth_bp.route("/delete/user", methods=["DELETE"])
@jwt_required()
@validate()
def delete_user_route(body: AuthRequest):
    """
    Delete user account from the system
    ---
    tags:
      - features/auth
    security:
      - BearerAuth: []
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
                description: The user's name
                example: "Test User"
              password:
                type: string
                description: Password
                example: "123456"
    responses:
      200:
        description: User account successfully deleted
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
                  nullable: true
                  example: null
      400:
        description: Validation error of incoming credentials (Pydantic)
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
      401:
        description: Unauthorized (missing or invalid JWT)
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                  example: "Missing Authorization Header"
      409:
        description: Deletion error (invalid password or user not found)
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
                  example: "Invalid password or user does not exist"
    """
    user_id = get_jwt_identity()

    user_name = body.user_name
    password = body.password

    result = auth_service.delete(user_name, password, int(user_id))

    if result.error:
        return DeleteResponse(error=result.error), 409
    else:
        return DeleteResponse(data=result.data), 200
