from enum import StrEnum


class ResultCodes(StrEnum):
    WORD_NOT_FOUND: str = "Word not found"
    UNEXPECTED_ERROR: str = "Unexpected error"
    ERROR_IN_FINDING: str = "Error while finding word"
