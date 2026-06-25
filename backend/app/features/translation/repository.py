from app.shared.extensions import db
from app.shared.dbmodels import Translation, User
from datetime import datetime


class TranslationRepository:
    def save_history(self, _word: str, _user_id: int, _time: datetime):
        try:
            translation = Translation(word=_word, user_id=_user_id, created_at=_time)
            db.session.add(translation)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise e

    def user_exists(self, user_id: int) -> bool:
        user = db.session.query(User).filter(User.id == user_id).first()
        return user is not None


translate_repo = TranslationRepository()
