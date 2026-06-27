from enum import StrEnum


class ResultCodes(StrEnum):
    DICTS_NOT_FOUND: str = "Dicts not found"
    UNEXPECTED_ERROR: str = "Unexpected error"
