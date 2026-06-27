from dataclasses import dataclass
from typing import TypeVar, Generic, Optional

T = TypeVar("T")


@dataclass
class BaseDTO(Generic[T]):
    success: bool
    data: Optional[T] = None
    error: Optional[str] = None
