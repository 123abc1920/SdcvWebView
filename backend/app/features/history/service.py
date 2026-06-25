import logging
from .repository import history_repo


class HistoryService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_history(self, user_id: int) -> dict:
        raw_translations = history_repo.get_history(user_id)

        translations = []
        for t in raw_translations:
            translations.append({"id": t.id, "word": t.word})

        return {"success": True, "data": translations}


history_service = HistoryService()
