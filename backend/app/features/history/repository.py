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


history_repo = HistoryRepository()
