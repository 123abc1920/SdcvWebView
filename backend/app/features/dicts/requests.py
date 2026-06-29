from pydantic import BaseModel, Field
from typing import List


class DictRequest(BaseModel):
    sdcv_type: str = Field(min_length=0, examples=["docker"])
    container_name: str = Field(min_length=0, examples=["sdcv-test"])
