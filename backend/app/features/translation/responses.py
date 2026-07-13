from pydantic import BaseModel, Field
from typing import List
from app.shared.validation import ApiResponse
from pydantic import BaseModel, Field, model_validator
from typing import List, Any


class TranslationData(BaseModel):
    dict_title: str = Field(
        ...,
        examples=["Eng-Rus"],
        description="The name of the dictionary.",
    )
    definition: str = Field(..., examples=["Word"], description="The word definition.")

    model_config = {"extra": "ignore", "populate_by_name": True}

    @model_validator(mode="before")
    @classmethod
    def map_dict_to_dict_title(cls, data: Any) -> Any:
        if isinstance(data, dict) and "dict" in data:
            data = {**data, "dict_title": data.pop("dict")}
        return data


TranslateResponse = ApiResponse[List[TranslationData]]
"""Type alias for the API response containing a list of translation data."""
