from app.shared.extensions import db
from app.shared.dbmodels import Translation


class HistoryRepository:
    def get_history(self, user_id: int) -> list[Translation]:
        return (
            db.session.query(Translation)
            .filter(Translation.user_id == user_id)
            .order_by(Translation.created_at.desc())
            .all()
        )

    def delete_history_item(self, id: int):
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
        return (
            db.session.query(Translation)
            .filter(Translation.id == translation_id)
            .first()
        )


history_repo = HistoryRepository()
