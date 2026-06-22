from app.shared.extensions import db
from app.shared.dbmodels import User
from .consts import ResultCodes


class AuthRepository:
    def add_user(self, _user_name: str, _password_hash: str, _is_admin: bool) -> str:
        try:
            user = User(
                name=_user_name, password_hash=_password_hash, is_admin=_is_admin
            )
            db.session.add(user)
            db.session.commit()
            return ResultCodes.OK
        except Exception as e:
            db.session.rollback()
            return str(e)

    def get_user(self, user_name: str) -> User:
        return db.session.query(User).filter(User.name == user_name).first()

    def count_users(self) -> int:
        return db.session.query(User).count()


auth_repo = AuthRepository()
