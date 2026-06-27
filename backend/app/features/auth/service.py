import logging
from .repository import auth_repo
from app.features.auth.consts import ResultCodes
import bcrypt
from flask_jwt_extended import create_access_token
from app.shared.dto import BaseDTO


class AuthService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def signup(self, user_name: str, password: str) -> BaseDTO[str]:
        user = auth_repo.get_user(user_name)

        if user:
            self.logger.error(ResultCodes.USER_EXISTS_ALREADY)
            return BaseDTO(success=True, error=ResultCodes.USER_EXISTS_ALREADY)

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

        is_admin = True
        if auth_repo.count_users() > 0:
            is_admin = False

        res = auth_repo.add_user(user_name, password_hash, is_admin)
        if res != ResultCodes.OK:
            self.logger.error(f"User was not created: {res}")
            return BaseDTO(success=False, error=ResultCodes.UNEXPECTED_ERROR)
        else:
            self.logger.info(f"User {user_name} created")
            user = auth_repo.get_user(user_name)
            token = self.create_token(user.id)
            return BaseDTO(success=True, data=token)

    def login(self, user_name: str, password: str) -> BaseDTO[str]:
        user = auth_repo.get_user(user_name)

        if user:
            password_hash = user.password_hash
            is_valid = self.is_password_valid(password, password_hash)

            if is_valid:
                self.logger.info(f"User {user_name} logged in")
                return BaseDTO(success=True, data=self.create_token(user.id))
            else:
                self.logger.warning(ResultCodes.PASSWORD_INCORRECT)
                return BaseDTO(success=False, error=ResultCodes.PASSWORD_INCORRECT)

        self.logger.warning(ResultCodes.USER_NOT_FOUND)
        return BaseDTO(success=False, error=ResultCodes.USER_NOT_FOUND)

    def delete(self, user_name: str, password: str, user_id: int) -> BaseDTO[None]:
        user = auth_repo.get_user(user_name)

        if user:
            if user.id != user_id:
                return BaseDTO(success=False, error=ResultCodes.DELETION_FORBIDDEN)

            password_hash = user.password_hash
            is_valid = self.is_password_valid(password, password_hash)

            if is_valid:
                result = auth_repo.delete_user(user_name)
                if result == ResultCodes.OK:
                    self.logger.info(f"User {user_name} deleted by {user_name}")

                    if auth_repo.count_users() > 0:
                        new_admin = auth_repo.get_first()
                        if new_admin:
                            auth_repo.set_admin(new_admin.name)
                            self.logger.info(f"User {user_name} is admin now")

                    return BaseDTO(success=True)
                else:
                    self.logger.error(f"Deletion error: {result}")
                    return BaseDTO(success=False, error=result)
            else:
                self.logger.warning(ResultCodes.PASSWORD_INCORRECT)
                return BaseDTO(success=False, error=ResultCodes.PASSWORD_INCORRECT)

        self.logger.warning(ResultCodes.USER_NOT_FOUND)
        return BaseDTO(success=False, error=ResultCodes.USER_NOT_FOUND)

    def get_user_data(self, user_id: int) -> BaseDTO[dict]:
        user = auth_repo.get_user_by_id(user_id)
        if user:
            return BaseDTO(success=True, data={"user_name": user.name})

        return BaseDTO(success=False, error=ResultCodes.USER_NOT_FOUND)

    def create_token(self, user_id: int) -> str:
        return create_access_token(identity=str(user_id))

    def is_password_valid(self, password: str, password_hash: str) -> bool:
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash.encode("utf-8"),
        )


auth_service = AuthService()
