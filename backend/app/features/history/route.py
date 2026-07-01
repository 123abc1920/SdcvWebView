from . import history_bp
from flask_jwt_extended import jwt_required, get_jwt_identity
from .service import history_service
from flask_pydantic import validate
from .requests import DeleteHistoryRequest
from .responses import HistoryResponse
from app.shared.validation import ApiResponse


@history_bp.route("/history", methods=["GET"])
@jwt_required()
@validate()
def get_history_route():
    """
    Get user history
    ---
    tags:
      - features/history
    security:
      - BearerAuth: []
    responses:
      200:
        description: Successful retrieval of history
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
        description: Server error / Business error
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
                  example: "Database error"
    """
    user_id = get_jwt_identity()

    result = history_service.get_history(user_id)

    if result.error:
        return (
            HistoryResponse(error=result.error),
            409,
        )
    else:
        return (
            HistoryResponse(data=result.data),
            200,
        )


@history_bp.route("/delete/history", methods=["DELETE"])
@jwt_required()
@validate()
def delete_history_item(body: DeleteHistoryRequest):
    """
    Delete entries from user history
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
                description: IDs to delete
                items:
                  type: integer
                example: [7, 8, 3]
    responses:
      200:
        description: Successful deletion
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
        description: Validation error of incoming JSON (Pydantic)
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
        description: Server error / Business error
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
                  example: "Database error"
    """
    user_id = get_jwt_identity()

    result = history_service.delete_history(body.ids, user_id)

    if result.error:
        return (
            ApiResponse(error=result.error),
            409,
        )
    else:
        return (
            ApiResponse(data=result.data),
            200,
        )
