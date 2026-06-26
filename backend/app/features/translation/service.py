import subprocess
import json
import logging
from .repository import translate_repo
from datetime import datetime
from .responses import TranslationData


class TranslateService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def translate(self, container_name: str, word: str, filters: list[str]) -> dict:
        try:
            u_filters = []
            for f in filters:
                u_filters.append("-u"),
                u_filters.append(f)

            result = subprocess.run(
                [
                    "docker",
                    "exec",
                    container_name,
                    "sdcv",
                    "--json-output",
                    "--exact-search",
                    str(word),
                    *u_filters,
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

    def save_history(self, word: str, user_id: int) -> bool:
        if translate_repo.user_exists(user_id):
            try:
                translate_repo.save_history(word, user_id, datetime.utcnow())
                self.logger.debug(f"Successfully save history for user {user_id}")
                return True
            except Exception as e:
                self.logger.error(
                    f"Error while saving history for user {user_id}: {str(e)}"
                )
                return False


translate_service = TranslateService()
