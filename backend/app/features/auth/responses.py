from app.shared.validation import ApiResponse
from pydantic import Field, BaseModel


class UserData(BaseModel):
    user_name: str = Field(..., examples=["Test User"])

    model_config = {"from_attributes": True}


UserDataResponse = ApiResponse[UserData]

DeleteResponse = ApiResponse[str]

JWTResponse = ApiResponse[str]
