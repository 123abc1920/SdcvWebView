from pydantic import BaseModel, Field
from typing import List
from app.shared.validation import ApiResponse


class HistoryItem(BaseModel):
    """Represents an individual entry within the translation history log."""

    id: int = Field(..., examples=[7], description="The unique ID of the history item.")
    """The unique ID of the history item."""

    word: str = Field(..., examples=["meet"], description="The translated word.")
    """The word that was translated and saved."""

    model_config = {"from_attributes": True}


HistoryResponse = ApiResponse[List[HistoryItem]]
"""Type alias for the API response containing a list of history items."""
