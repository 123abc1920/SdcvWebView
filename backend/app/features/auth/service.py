import logging
from .repository import auth_repo
from app.features.auth.consts import ResultCodes
import bcrypt
from flask_jwt_extended import create_access_token
from app.shared.dto import BaseDTO
from .dto import UserDTO


class AuthService:
    """
    Service for user authentication.
    """

    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def signup(self, user_name: str, password: str) -> BaseDTO[str]:
        """
        Registers users in the system.

        Args:
            user_name (str): The name of the user.
            password (str): The user's password.

        Returns:
            BaseDTO: The data transfer object containing registration results.
        """
        user = auth_repo.get_user(user_name)

        if user:
            self.logger.error(ResultCodes.USER_EXISTS_ALREADY)
            return BaseDTO(error=ResultCodes.USER_EXISTS_ALREADY)

        salt = bcrypt.gensalt()
        password_hash = bcrypt.hashpw(password.encode("utf-8"), salt)

        is_admin = True
        if auth_repo.count_users() > 0:
            is_admin = False

        try:
            auth_repo.add_user(user_name, password_hash, is_admin)
            self.logger.info(f"User {user_name} created")
            user = auth_repo.get_user(user_name)
            token = self._create_token(user.id)
            return BaseDTO(data=token)
        except Exception as e:
            self.logger.error(f"User was not created: {str(e)}")
            return BaseDTO(error=ResultCodes.UNEXPECTED_ERROR)

    def login(self, user_name: str, password: str) -> BaseDTO[str]:
        """
        Authenticates users and performs system login.

        Args:
            user_name (str): The name of the user.
            password (str): The user's password.

        Returns:
            BaseDTO: The data transfer object containing authentication results.
        """
        user = auth_repo.get_user(user_name)

        if user:
            password_hash = user.password_hash
            is_valid = self._is_password_valid(password, password_hash)

            if is_valid:
                self.logger.info(f"User {user_name} logged in")
                return BaseDTO(data=self._create_token(user.id))
            else:
                self.logger.warning(ResultCodes.PASSWORD_INCORRECT)
                return BaseDTO(error=ResultCodes.PASSWORD_INCORRECT)

        self.logger.warning(ResultCodes.USER_NOT_FOUND)
        return BaseDTO(error=ResultCodes.USER_NOT_FOUND)

    def delete(self, user_name: str, password: str, user_id: int) -> BaseDTO[None]:
        """
        Deletes a user from the system.

        Args:
            user_name (str): The name of the user.
            password (str): The user's password.
            user_id (int): The unique ID of the user.

        Returns:
            BaseDTO: The data transfer object containing deletion results.
        """
        user = auth_repo.get_user(user_name)

        if user:
            if user.id != user_id:
                return BaseDTO(error=ResultCodes.DELETION_FORBIDDEN)

            password_hash = user.password_hash
            is_valid = self._is_password_valid(password, password_hash)

            if is_valid:
                try:
                    auth_repo.delete_user(user_name)
                    self.logger.info(f"User {user_name} deleted by {user_name}")

                    if auth_repo.count_users() > 0:
                        new_admin = auth_repo.get_first()
                        if new_admin:
                            auth_repo.set_admin(new_admin.name)
                            self.logger.info(f"User {new_admin.name} is admin now")

                    return BaseDTO()
                except Exception as e:
                    self.logger.error(f"Deletion error: {str(e)}")
                    return BaseDTO(error=str(e))
            else:
                self.logger.warning(ResultCodes.PASSWORD_INCORRECT)
                return BaseDTO(error=ResultCodes.PASSWORD_INCORRECT)

        self.logger.warning(ResultCodes.USER_NOT_FOUND)
        return BaseDTO(error=ResultCodes.USER_NOT_FOUND)

    def get_user_data(self, user_id: int) -> BaseDTO[UserDTO]:
        """
        Retrieves user data.

        Args:
            user_id (int): The unique ID of the user.

        Returns:
            BaseDTO: The data transfer object containing the user data.
        """
        user = auth_repo.get_user_by_id(user_id)
        if user:
            return BaseDTO(data=UserDTO(user_name=user.name))

        return BaseDTO(error=ResultCodes.USER_NOT_FOUND)

    def _create_token(self, user_id: int) -> str:
        """
        Generates a JWT token for a user.

        Args:
            user_id (int): The unique ID of the user.

        Returns:
            str: The generated JWT token string.
        """
        return create_access_token(identity=str(user_id))

    def _is_password_valid(self, password: str, password_hash: bytes) -> bool:
        """
        Verifies whether the password is correct.

        Args:
            password (str): The plain-text password to verify.
            password_hash (bytes): The hashed password bytes to compare against.

        Returns:
            bool: True if the password matches the hash, False otherwise.
        """
        return bcrypt.checkpw(
            password.encode("utf-8"),
            password_hash,
        )


auth_service = AuthService()
