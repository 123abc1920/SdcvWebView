from . import dicts_bp
from .service import dicts_service
from flask_pydantic import validate
from .responses import DictsResponse
from .requests import DictRequest
from app.shared.sdcv_engine import create_engine
import logging

logger = logging.getLogger(__name__)


@dicts_bp.route("/dicts", methods=["POST"])
@validate()
def list_dicts(body: DictRequest):
    """
    Получить список всех доступных словарей
    ---
    tags:
      - features/dicts
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - sdcv_type
            properties:
              sdcv_type:
                type: string
                description: Откуда запускать sdcv
                example: "docker"
              container_name:
                type: string
                description: Имя контейнера, если sdcv в docker
                example: "sdcv-test"
    responses:
      200:
        description: Успешное получение списка словарей
        content:
          application/json:
            schema:
              type: object
              required: [data, error]
              properties:
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
              required: [data, error]
              properties:
                data:
                  type: object
                  nullable: true
                  example: null
                error:
                  type: string
                  example: "Failed to fetch dictionaries from container"
    """
    sdcv_type = body.sdcv_type
    container_name = body.container_name

    engine = None
    try:
        engine = create_engine(sdcv_type, container_name)
    except Exception as e:
        logger.error(str(e))
        return DictsResponse(error=str(e)), 409

    result = dicts_service.get_all(engine)

    if result.error:
        return DictsResponse(error=result.error), 409
    else:
        return DictsResponse(data=result.data), 200
