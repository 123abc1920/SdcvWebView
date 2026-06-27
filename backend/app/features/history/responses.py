from pydantic import BaseModel, Field
from typing import List
from app.shared.validation import ApiResponse


class HistoryItemSchema(BaseModel):
    id: int = Field(..., examples=[7])
    word: str = Field(..., examples=["meet"])

    model_config = {"from_attributes": True}


HistoryResponseSchema = ApiResponse[List[HistoryItemSchema]]
