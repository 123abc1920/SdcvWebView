from app.shared.validation import ApiResponse
from pydantic import Field, BaseModel


class UserData(BaseModel):
    """
    User's data
    """

    user_name: str = Field(
        ...,
        examples=["Test User"],
        description="The unique name of the user.",
    )
    """The unique name of the user."""

    model_config = {"from_attributes": True}


UserDataResponse = ApiResponse[UserData]
"""User data response"""

DeleteResponse = ApiResponse[str]
"""Delete user response"""

JWTResponse = ApiResponse[str]
"""Giving JWT response"""
