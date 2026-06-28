import subprocess
import json
import logging
from .repository import translate_repo
from datetime import datetime
from .responses import TranslationData
from app.shared.dto import BaseDTO
from typing import List
from .consts import ResultCodes


class TranslateService:

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def translate(
        self, container_name: str, word: str, filters: list[str]
    ) -> BaseDTO[List[TranslationData]]:
        if word == "" or word.isspace() or word is None:
            self.logger.warning("Word is empty")
            return BaseDTO(error=ResultCodes.WORD_NOT_FOUND)

        word = word.strip().replace(" ", "").lower()

        try:
            u_filters = []
            for f in filters:
                u_filters.append("-u")
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
                return BaseDTO(data=[item.model_dump() for item in validated_data])
            elif result.returncode == 2:
                self.logger.warning("Word not found in dicts")
                return BaseDTO(error=ResultCodes.WORD_NOT_FOUND)
            else:
                self.logger.error(result.stderr)
                return BaseDTO(error=ResultCodes.UNEXPECTED_ERROR)

        except subprocess.TimeoutExpired:
            self.logger.error("Timeout")
            return BaseDTO(error=ResultCodes.ERROR_IN_FINDING)
        except Exception as e:
            self.logger.error(str(e))
            return BaseDTO(error=ResultCodes.UNEXPECTED_ERROR)

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
        return False


translate_service = TranslateService()
