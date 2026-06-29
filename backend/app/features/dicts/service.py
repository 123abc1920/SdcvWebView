import logging
from app.shared.dto import BaseDTO
from .consts import ResultCodes
import subprocess
from app.shared.sdcv_engine import BaseSdcvEngine


class DictsService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all(self, engine: BaseSdcvEngine) -> BaseDTO[list]:
        try:
            result = engine.list()

            if result.returncode == 0:
                stdout = result.stdout
                data = stdout.split("\n")

                dicts = []
                for i in range(1, len(data) - 1):
                    dict_name = data[i].rsplit(None, 1)[0]
                    dicts.append(dict_name)

                return BaseDTO(data=dicts)
            else:
                self.logger.error(result.stderr)
                return BaseDTO(error=ResultCodes.UNEXPECTED_ERROR)

        except subprocess.TimeoutExpired:
            self.logger.error("Timeout")
            return BaseDTO(error=ResultCodes.DICTS_NOT_FOUND)
        except Exception as e:
            self.logger.error(str(e))
            return BaseDTO(error=ResultCodes.UNEXPECTED_ERROR)


dicts_service = DictsService()
