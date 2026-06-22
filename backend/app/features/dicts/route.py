from . import dicts_bp
from .service import dicts_service

SDCV_TEST_CONTAINER = "sdcv-test"


@dicts_bp.route("/dicts", methods=["GET"])
def list_dicts():
    """
    Получить список всех доступных словарей
    ---
    tags:
      - features/dicts
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
    result = dicts_service.get_all(SDCV_TEST_CONTAINER)

    if result["success"] == True:
        return {"data": result["data"]}, 200
    else:
        return {"message": result["data"]}, 409
