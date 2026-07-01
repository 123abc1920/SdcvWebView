from app.shared.extensions import db
from app.shared.dbmodels import Translation


class HistoryRepository:
    """
    Repository for managing user translation history records in the database.
    """

    def get_history(self, user_id: int) -> list[Translation]:
        """
        Retrieves the translation history for a specific user.

        Args:
            user_id (int): The unique ID of the user.

        Returns:
            list[Translation]: A list of translation history elements.
        """
        return (
            db.session.query(Translation)
            .filter(Translation.user_id == user_id)
            .order_by(Translation.created_at.desc())
            .all()
        )

    def delete_history_item(self, id: int):
        """
        Deletes a specific element from the user's translation history.

        Args:
            id (int): The unique ID of the element to delete.
        """
        try:
            translation = (
                db.session.query(Translation).filter(Translation.id == id).first()
            )
            if translation:
                db.session.delete(translation)
                db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def get_history_item(self, translation_id: int) -> Translation:
        """
        Retrieves a specific translation history element by its ID.

        Args:
            translation_id (int): The unique ID of the translation element.

        Returns:
            Translation: The requested translation history element.
        """
        return (
            db.session.query(Translation)
            .filter(Translation.id == translation_id)
            .first()
        )


history_repo = HistoryRepository()
