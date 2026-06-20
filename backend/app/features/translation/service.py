import subprocess
import json
from pydantic import BaseModel, validator


class TranslationData(BaseModel):
    dict: str
    definition: str

    class Config:
        extra = "ignore"


class TranslateService:
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

            print(result)

            if result.returncode == 0:
                data = json.loads(result.stdout)

                validated_data = [TranslationData(**item) for item in data]
                return {
                    "success": True,
                    "data": [item.model_dump() for item in validated_data],
                }
            elif result.returncode == 2:
                return {
                    "success": False,
                    "data": "Слово не найдено",
                }
            else:
                return {"success": False, "data": result.stderr}

        except subprocess.TimeoutExpired:
            return {"success": False, "data": "Timeout"}
        except Exception as e:
            return {"success": False, "data": str(e)}


translate_service = TranslateService()
