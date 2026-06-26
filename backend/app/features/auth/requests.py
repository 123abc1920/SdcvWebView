from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    user_name: str = Field(..., min_length=1, examples=["Test User"])
    password: str = Field(..., min_length=1, examples=["123456"])
