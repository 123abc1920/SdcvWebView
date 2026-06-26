from pydantic import BaseModel, Field
from typing import List


class TranslateRequest(BaseModel):
    word: str = Field(..., min_length=0, examples=["meet"])
    filters: List[str] = Field(
        default=[], examples=[["Mueller7GPL", "Full English-Russian"]]
    )
