import logging
import subprocess


class DictsService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_all(self, container_name: str) -> dict:
        try:
            result = subprocess.run(
                ["docker", "exec", container_name, "sdcv", "-l"],
                capture_output=True,
                text=True,
                encoding="utf-8",
                timeout=10,
            )

            if result.returncode == 0:
                data = result.stdout
                data = data.split("\n")

                dicts = []
                for i in range(1, len(data) - 1):
                    dict_name = data[i].rsplit(None, 1)[0]
                    dicts.append(dict_name)

                return {"success": True, "data": dicts}
            else:
                self.logger.error(result.stderr)
                return {"success": False, "data": "Непредвиденная ошибка"}

        except subprocess.TimeoutExpired:
            self.logger.error("Timeout")
            return {"success": False, "data": "Словари не найдены"}
        except Exception as e:
            self.logger.error(str(e))


dicts_service = DictsService()
