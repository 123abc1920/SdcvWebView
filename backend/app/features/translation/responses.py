from pydantic import BaseModel
from typing import List
from app.shared.validation import ApiResponse


class TranslationData(BaseModel):
    dict: str
    definition: str

    model_config = {"extra": "ignore"}


TranslateResponseSchema = ApiResponse[List[TranslationData]]
