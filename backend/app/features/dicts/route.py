from . import dicts_bp
from .service import dicts_service
from flask_pydantic import validate
from .responses import DictsResponse

SDCV_TEST_CONTAINER = "sdcv-test"


@dicts_bp.route("/dicts", methods=["GET"])
@validate()
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
              required: [success, data, error]
              properties:
                success:
                  type: boolean
                  example: true
                data:
                  type: array
                  description: Список названий словарей, доступных в sdcv
                  items:
                    type: string
                  example: ["Mueller7GPL", "Full English-Russian", "LingvoUniversal"]
                error:
                  type: string
                  nullable: true
                  example: null
      409:
        description: Внутренняя ошибка сервера при обращении к контейнеру sdcv
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
                  example: "Failed to fetch dictionaries from container"
    """
    result = dicts_service.get_all(SDCV_TEST_CONTAINER)

    if result["success"] == True:
        return DictsResponse(success=True, data=result["data"]), 200
    else:
        return DictsResponse(success=False, error=result["data"]), 409
