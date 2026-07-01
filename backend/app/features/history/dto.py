from dataclasses import dataclass


@dataclass
class TranslationDTO:
    """Data transfer object representing a completed translation entry."""

    id: int
    """The unique identifier of the translation."""

    word: str
    """The translated word."""
