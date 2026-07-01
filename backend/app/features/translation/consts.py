from enum import StrEnum


class ResultCodes(StrEnum):
    """Operation execution result codes."""

    WORD_NOT_FOUND = "Word not found"
    """The requested word was not found in the dictionary."""

    UNEXPECTED_ERROR = "Unexpected error"
    """An unhandled or unexpected error occurred during execution."""

    ERROR_IN_FINDING = "Error while finding word"
    """An error occurred specifically during the dictionary lookup process."""
