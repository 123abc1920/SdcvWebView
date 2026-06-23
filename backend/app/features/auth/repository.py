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

    def delete_user(self, user_name: str) -> str:
        user = self.get_user(user_name)

        try:
            db.session.delete(user)
            db.session.commit()
            return ResultCodes.OK
        except Exception as e:
            db.session.rollback()
            return str(e)

    def set_admin(self, user_name: str):
        user = self.get_user(user_name)
        user.is_admin = True
        db.session.commit()

    def get_first(self) -> User:
        return db.session.query(User).order_by(User.id.asc()).first()


auth_repo = AuthRepository()
