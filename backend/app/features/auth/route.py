from . import auth_bp


@auth_bp.route("/login", methods=["POST"])
def login_route():
    """
    Зарегистрироваться в системе
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
