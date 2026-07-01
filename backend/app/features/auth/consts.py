from enum import StrEnum


from enum import StrEnum


class ResultCodes(StrEnum):
    """Operation execution result codes."""

    OK: str = "OK"
    """Successful result."""

    USER_EXISTS_ALREADY: str = "User already exists"
    """The username or email is taken during registration."""

    PASSWORD_INCORRECT: str = "Incorrect password"
    """The provided password does not match the stored hash."""

    UNEXPECTED_ERROR: str = "Unexpected error"
    """Various errors worth checking in logs."""

    USER_NOT_FOUND: str = "User not found"
    """The requested user ID does not exist in the database."""

    DELETION_FORBIDDEN: str = "No permission to delete"
    """Removal prohibited due to insufficient user privileges."""
