from pydantic import BaseModel, Field
from typing import List


class DeleteHistoryRequestSchema(BaseModel):
    ids: List[int] = Field(..., min_length=0, examples=[[7, 8, 3]])
