from app.shared.extensions import db
from app.shared.dbmodels import Translation, User
from datetime import datetime


class TranslationRepository:
    """
    Repository for managing and saving translation history.
    """

    def save_history(self, _word: str, _user_id: int, _time: datetime):
        """
        Adds a new translation history item.

        Args:
            _word (str): The word that was requested.
            _user_id (int): The unique ID of the user.
            _time (datetime): The timestamp of the request.

        Raises:
            Exception: If the database record creation fails.
        """
        try:
            translation = Translation(word=_word, user_id=_user_id, created_at=_time)
            db.session.add(translation)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def user_exists(self, user_id: int) -> bool:
        """
        Checks if a user already exists in the system.

        Args:
            _user_id (int): The unique ID of the user to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        user = db.session.query(User).filter(User.id == user_id).first()
        return user is not None


translate_repo = TranslationRepository()
