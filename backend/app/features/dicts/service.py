import logging
import subprocess
from app.shared.dto import BaseDTO
from .consts import ResultCodes


class DictsService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all(self, container_name: str) -> BaseDTO[list]:
        try:
            result = subprocess.run(
                ["docker", "exec", container_name, "sdcv", "-l"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=10,
            )

            if result.returncode == 0:
                stdout = result.stdout
                data = stdout.split("\n")

                dicts = []
                for i in range(1, len(data) - 1):
                    dict_name = data[i].rsplit(None, 1)[0]
                    dicts.append(dict_name)

                return BaseDTO(success=True, data=dicts)
            else:
                self.logger.error(result.stderr)
                return BaseDTO(success=False, data=ResultCodes.UNEXPECTED_ERROR)

        except subprocess.TimeoutExpired:
            self.logger.error("Timeout")
            return BaseDTO(success=False, error=ResultCodes.DICTS_NOT_FOUND)
        except Exception as e:
            self.logger.error(str(e))
            return BaseDTO(success=False, error=ResultCodes.UNEXPECTED_ERROR)


dicts_service = DictsService()
