import logging
from .repository import history_repo
from app.shared.dto import BaseDTO
from typing import List
from .dto import TranslationDTO


class HistoryService:
    """
    Service for managing user translation history data.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def get_history(self, user_id: int) -> BaseDTO[List[TranslationDTO]]:
        """
        Retrieves the translation history for a specific user.

        Args:
            user_id (int): The unique ID of the user.

        Returns:
            BaseDTO[list[TranslationDTO]]: The data transfer object containing the list of translation history entries.
        """
        raw_translations = history_repo.get_history(user_id)

        translations = []
        for t in raw_translations:
            translations.append(TranslationDTO(id=t.id, word=t.word))

        return BaseDTO(data=translations)

    def delete_history(self, ids: list, user_id: int) -> BaseDTO[None]:
        """
        Deletes specific items from a user's translation history.

        Args:
            ids (list[int]): A list of history entry IDs to be deleted.
            user_id (int): The unique ID of the user.

        Returns:
            BaseDTO[None]: The data transfer object containing the operation results.
        """
        for id in ids:
            if self.is_user_owns_history_item(user_id, id):
                try:
                    history_repo.delete_history_item(id)
                    self.logger.info(f"Successfully delete history item {id}")
                except Exception as e:
                    self.logger.error(
                        f"Error while history item {id} deletion: {str(e)}"
                    )
            else:
                self.logger.warning(f"User {user_id} does not own item {id}")

        return BaseDTO(data=None)

    def is_user_owns_history_item(self, user_id: int, translation_id: int) -> bool:
        """
        Checks if a specific history element belongs to a given user.

        Args:
            user_id (int): The unique ID of the user.
            translation_id (int): The unique ID of the translation entry.

        Returns:
            bool: True if the user owns the history element, False otherwise.
        """
        translation = history_repo.get_history_item(translation_id)

        if translation and int(translation.user_id) == int(user_id):
            return True

        return False


history_service = HistoryService()
