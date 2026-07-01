from enum import StrEnum


class ResultCodes(StrEnum):
    """Operation execution result codes."""

    DICTS_NOT_FOUND = "Dicts not found"
    """No matching dictionaries were found in the system."""

    UNEXPECTED_ERROR = "Unexpected error"
    """An unhandled or unexpected error occurred during execution."""
