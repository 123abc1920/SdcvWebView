import subprocess
import json
from pydantic import BaseModel
import logging


class TranslationData(BaseModel):
    dict: str
    definition: str

    class Config:
        extra = "ignore"


class TranslateService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def translate(self, container_name: str, word: str) -> dict:
        try:
            result = subprocess.run(
                [
                    "docker",
                    "exec",
                    container_name,
                    "sdcv",
                    "--json-output",
                    "--exact-search",
                    str(word),
                ],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=10,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)

                validated_data = [TranslationData(**item) for item in data]

                self.logger.info("Word succsessfully found")
                return {
                    "success": True,
                    "data": [item.model_dump() for item in validated_data],
                }
            elif result.returncode == 2:
                self.logger.warning("Word not found in dicts")
                return {
                    "success": False,
                    "data": "Слово не найдено",
                }
            else:
                self.logger.error(result.stderr)
                return {"success": False, "data": "Непредвиденная ошибка"}

        except subprocess.TimeoutExpired:
            self.logger.error("Timeout")
            return {"success": False, "data": "Ошибка поиска слова"}
        except Exception as e:
            self.logger.error(str(e))
            return {"success": False, "data": "Непредвиденная ошибка"}


translate_service = TranslateService()
