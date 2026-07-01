from pydantic import BaseModel, Field


class AuthRequest(BaseModel):
    """
    Represents an authorization request payload.
    """

    user_name: str = Field(
        ...,
        description="The unique name of the user.",
        examples=["Test User"],
    )

    password: str = Field(
        ...,
        min_length=1,
        description="The plain text password of the user.",
        examples=["123456"],
    )
