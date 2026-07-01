from app.shared.extensions import db
from app.shared.dbmodels import User


class AuthRepository:
    """
    Repository for interacting with user database tables.
    """

    def add_user(self, _user_name: str, _password_hash: str, _is_admin: bool):
        """
        Adds a new user.

        Args:
            _user_name (str): The user's name.
            _password_hash (str): The password hash string.
            _is_admin (bool): Indicates whether the user is a server administrator.

        Raises:
            Exception: If the record creation fails.
        """
        try:
            user = User(
                name=_user_name, password_hash=_password_hash, is_admin=_is_admin
            )
            db.session.add(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

    def get_user(self, user_name: str) -> User:
        """
        Returns a user from the database by name.

        Args:
            user_name (str): The name of the user.

        Returns:
            User: The found user object.
        """
        return db.session.query(User).filter(User.name == user_name).first()

    def get_user_by_id(self, user_id: int) -> User:
        """
        Returns a user from the database by id.

        Args:
            user_id (int): The id of the user.

        Returns:
            User: The found user object.
        """
        return db.session.query(User).filter(User.id == user_id).first()

    def count_users(self) -> int:
        """
        Counts the number of users.

        Returns:
            int: The total count of users.
        """
        return db.session.query(User).count()

    def delete_user(self, user_name: str):
        """
        Deletes a user.

        Args:
            user_name (str): The name of the user.

        Raises:
            Exception: If the user deletion fails.
        """
        user = self.get_user(user_name)

        try:
            db.session.delete(user)
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            raise Exception(str(e))

    def set_admin(self, user_name: str):
        """
        Grants server administrator privileges to a user in the database.

        Args:
            user_name (str): The name of the user.
        """
        user = self.get_user(user_name)
        if user:
            user.is_admin = True
            db.session.commit()

    def get_first(self) -> User:
        """
        Returns the first user created in the database (ordered by ID).

        Returns:
            Optional[User]: The first user object, or None if the table is empty.
        """
        return db.session.query(User).order_by(User.id.asc()).first()


auth_repo = AuthRepository()
