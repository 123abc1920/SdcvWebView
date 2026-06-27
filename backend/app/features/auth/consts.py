from enum import StrEnum


class ResultCodes(StrEnum):
    OK: str = "OK"
    USER_EXISTS_ALREADY: str = "User already exists"
    PASSWORD_INCORRECT: str = "Incorrect password"
    UNEXPECTED_ERROR: str = "Unexpected error"
    USER_NOT_FOUND: str = "User not found"
    DELETION_FORBIDDEN: str = "No permission to delete user"
