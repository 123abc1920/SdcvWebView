import subprocess
import json
from pydantic import BaseModel, validator


class TranslationData(BaseModel):
    dict_name: str
    content: str


class TranslateService:
    def translate(self, container_name: str, word: str) -> dict:
        try:
            result = subprocess.run(
                ["docker", "exec", container_name, "sdcv", "--json-output", word],
                capture_output=True,
                text=True,
                timeout=10,
            )

            if result.returncode == 0:
                data = json.loads(result.stdout)

                validated_data = [TranslationData(**item) for item in data]
                return {
                    "success": True,
                    "data": [item.dict() for item in validated_data],
                }
            else:
                return {"success": False, "data": result.stderr}

        except subprocess.TimeoutExpired:
            return {"success": False, "data": "Timeout"}
        except Exception as e:
            return {"success": False, "data": str(e)}


translate_service = TranslateService()
