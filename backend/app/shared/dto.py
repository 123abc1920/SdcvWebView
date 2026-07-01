from dataclasses import dataclass
from typing import TypeVar, Generic, Optional

from typing import TypeVar, Generic, Optional
from dataclasses import dataclass

T = TypeVar("T")
"""Type variable representing the payload data type within the DTO."""


@dataclass
class BaseDTO(Generic[T]):
    """
    Generic Data Transfer Object used for wrapping API responses.
    """

    data: Optional[T] = None
    """The payload data of type T, or None if an error occurred."""

    error: Optional[str] = None
    """The error description, or None if the operation was successful."""
