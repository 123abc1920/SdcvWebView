from pydantic import BaseModel, Field
from typing import List


class DeleteHistoryRequest(BaseModel):
    """
    Represents a request payload for deleting specific items from the translation history.
    """

    ids: List[int] = Field(
        ...,
        min_length=1,
        examples=[[7, 8, 3]],
        description="A list of unique IDs of the history items to be deleted.",
    )
    """A list of unique IDs of the history items to be deleted."""
