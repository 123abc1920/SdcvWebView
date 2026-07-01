from pydantic import BaseModel, Field
from typing import List


class DictRequest(BaseModel):
    """
    Represents a request to retrieve the list of available dictionaries.
    """

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
