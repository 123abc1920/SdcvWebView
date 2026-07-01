from pydantic import BaseModel, Field
from typing import List


class TranslateRequest(BaseModel):
    """Represents the request payload for a word translation."""

    word: str = Field(
        ..., min_length=0, examples=["meet"], description="The word to be translated."
    )
    """The word to be translated."""

    filters: List[str] = Field(
        default=[],
        examples=[["Mueller7GPL", "Full English-Russian"]],
        description="A list of specific dictionary names to filter the results.",
    )
    """A list of specific dictionary names to filter the results."""

    sdcv_type: str = Field(
        min_length=0,
        examples=["docker"],
        description="The deployment type of the sdcv application.",
    )
    """The deployment type of the sdcv application."""

    container_name: str = Field(
        min_length=0,
        examples=["sdcv-test"],
        description="The name of the sdcv container, if deployed inside Docker.",
    )
    """The name of the sdcv container, if deployed inside Docker."""
