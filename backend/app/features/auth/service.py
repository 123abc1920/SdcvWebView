import logging
from .repository import auth_repo
from app.features.auth.consts import ResultCodes
import bcrypt
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity,
)


class AuthService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def signup(self, user_name: str, password: str) -> dict:
        user = auth_repo.get_user(user_name)

        if user:
            self.logger.error(ResultCodes.USER_EXISTS_ALREADY)
            return {"success": False, "data": ResultCodes.USER_EXISTS_ALREADY}

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

        is_admin = True
        if auth_repo.count_users() > 0:
            is_admin = False

        res = auth_repo.add_user(user_name, password_hash, is_admin)
        if res != ResultCodes.OK:
            self.logger.error(f"User was not created: {res}")
            return {"success": False, "data": None}
        else:
            self.logger.info(f"User {user_name} created")
            user = auth_repo.get_user(user_name)
            token = self.create_token(user.id)
            return {"success": True, "data": token}

    def login(self, user_name, password_hash):
        pass

    def delete(self, user_name, password_hash):
        pass

    def create_token(self, user_id: int) -> str:
        return create_access_token(identity=user_id)


auth_service = AuthService()
