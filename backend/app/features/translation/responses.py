from pydantic import BaseModel, Field
from typing import List
from app.shared.validation import ApiResponse


from pydantic import BaseModel, Field
from typing import List


class TranslationData(BaseModel):
    """Represents the structured translation data returned from a dictionary lookup."""

    dict: str = Field(
        ..., examples=["Eng-Rus"], description="The name of the dictionary."
    )
    """The dictionary name."""

    definition: str = Field(..., examples=["Word"], description="The word definition.")
    """The word definition."""

    model_config = {"extra": "ignore"}


TranslateResponse = ApiResponse[List[TranslationData]]
"""Type alias for the API response containing a list of translation data."""
